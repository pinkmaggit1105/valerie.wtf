// The rules every pet lives by: stats, the egg, growing up, moods. No page code in here, so the
// landing page can use it to show how each pet is doing without opening their page.
(function () {
    // per-hour changes. a full tummy lasts about half a day.
    const DECAY = {
        awake:  { food: -6, fun: -5, clean: -3, energy: -4 },
        asleep: { food: -3, fun: -1, clean: -1, energy: 20 }
    };

    // the egg cools off over a few hours, and hatches after about 2.5 warm hours
    const EGG = { cooling: 15, growth: 40, cold: 30 };

    const MAX_CATCHUP_H = 24 * 14;

    const STATS = { food: "Food", fun: "Fun", clean: "Clean", energy: "Energy", health: "Health" };
    const EGG_STATS = { warmth: "Warmth", progress: "Hatching" };

    const clamp = v => Math.max(0, Math.min(100, v));

    function fresh() {
        const now = Date.now();
        return {
            laid: now, born: now, last: now, hatched: false, asleep: false, overfedUntil: 0, grown: false,
            egg: { warmth: 70, progress: 0 },
            stats: { food: 70, fun: 70, clean: 90, energy: 80, health: 100 },
            poops: 0, nextPoop: 0, flags: {},
            wearing: {}, counts: {}, catches: {}, log: []
        };
    }

    function load(cfg) {
        let s = null;
        try { s = JSON.parse(localStorage.getItem(cfg.saveKey)); } catch (e) {}
        const isNew = !s || !s.stats;
        if (isNew) s = fresh();
        // fill in anything older saves don't have yet
        if (s.hatched === undefined) s.hatched = true;
        s.egg ||= { warmth: 0, progress: 100 };
        s.wearing ||= {};
        s.catches ||= {};
        s.flags ||= {};
        if (s.goldenFish) { s.flags.golden = true; delete s.goldenFish; }
        s.poops ??= 0;
        s.nextPoop ??= 0;
        return { state: s, isNew };
    }

    function save(cfg, s) { try { localStorage.setItem(cfg.saveKey, JSON.stringify(s)); } catch (e) {} }

    const ageMs = s => Date.now() - s.born;
    const isBaby = (s, cfg) => ageMs(s) < cfg.growUpHours * 36e5;
    const stage = (s, cfg) => !s.hatched ? "egg" : isBaby(s, cfg) ? "baby" : "adult";

    function bump(s, stat, by) { s.stats[stat] = clamp(s.stats[stat] + by); }

    function logEvent(s, msg) {
        s.log.push({ t: Date.now(), msg });
        if (s.log.length > 50) s.log.shift();
    }

    // Advance time in small steps so health reacts to stats crossing thresholds mid-absence.
    // Returns what happened, so the page can make a fuss about it.
    function tick(s, cfg) {
        const now = Date.now();
        const events = { hatched: false, grewUp: false, pooped: false };
        let hours = Math.min((now - s.last) / 36e5, MAX_CATCHUP_H);
        s.last = now;
        while (hours > 0) {
            const h = Math.min(hours, 0.25);
            hours -= h;
            if (!s.hatched) {
                const e = s.egg;
                e.warmth = clamp(e.warmth - EGG.cooling * h);
                if (e.warmth >= EGG.cold) e.progress = Math.min(100, e.progress + EGG.growth * h);
                if (e.progress >= 100) {
                    s.hatched = true;
                    s.born = now - hours * 36e5;
                    events.hatched = true;
                    logEvent(s, cfg.text.log.hatched);
                }
                continue;
            }
            const st = s.stats;
            for (const [k, v] of Object.entries(DECAY[s.asleep ? "asleep" : "awake"])) bump(s, k, v * h);
            // poop left lying around makes them dirty, and a lot of it makes them ill
            if (s.poops) bump(s, "clean", -2 * s.poops * h);
            if (s.poops >= 2) bump(s, "health", -1 * h);
            if (st.food < 15 || st.clean < 15) bump(s, "health", -6 * h);
            else if (st.food > 40 && st.clean > 40) bump(s, "health", 3 * h);
            if (s.asleep && st.energy >= 100) { s.asleep = false; logEvent(s, cfg.text.log.woke); }
        }
        if (s.hatched && s.nextPoop && now >= s.nextPoop && !s.asleep) {
            s.nextPoop = 0;
            if (s.poops < 3) {
                s.poops++;
                events.pooped = true;
                logEvent(s, cfg.text.log.pooped);
            }
        }
        if (s.hatched && !s.grown && !isBaby(s, cfg)) {
            s.grown = true;
            events.grewUp = true;
            logEvent(s, cfg.text.log.grewUp);
        }
        return events;
    }

    const crackLevel = s => s.egg.progress >= 75 ? 2 : s.egg.progress >= 40 ? 1 : 0;
    const eggCold = s => s.egg.warmth < EGG.cold;

    // which idle sprite fits how they feel right now
    function mood(s) {
        if (!s.hatched) return `egg_${eggCold(s) ? "cold_" : ""}${crackLevel(s)}`;
        const st = s.stats;
        if (s.asleep) return "sleep";
        if (st.health < 40) return "idle_sick";
        if (Date.now() < s.overfedUntil) return "idle_overfed";
        if (st.food < 30) return "idle_hungry";
        if (st.clean < 30) return "idle_stinky";
        if (st.energy < 20) return "idle_sleepy";
        if (st.fun < 30) return "idle_sad";
        if (Object.values(st).every(v => v >= 80)) return "idle_ecstatic";
        if (st.fun >= 55) return "idle_happy";
        return "idle_neutral";
    }

    // [chip text, chip level, hint]
    function moodInfo(s, cfg) {
        if (s.hatched) {
            const m = cfg.moods[mood(s)];
            if (s.poops && !s.asleep && mood(s) !== "idle_sick") return [m[0], m[1], cfg.text.poopHint];
            return m;
        }
        if (eggCold(s)) return cfg.eggMoods.cold;
        if (crackLevel(s) === 2) return cfg.eggMoods.wiggling;
        return cfg.eggMoods.egg;
    }

    function ageText(s, cfg) {
        if (!s.hatched) return cfg.text.eggAge;
        const mins = Math.floor(ageMs(s) / 6e4);
        const d = Math.floor(mins / 1440), h = Math.floor(mins / 60) % 24, m = mins % 60;
        const old = d ? `${d}d ${h}h old` : h ? `${h}h ${m}m old` : `${m}m old`;
        return isBaby(s, cfg) ? `${cfg.stages.baby} · ${old}` : old;
    }

    // egg and hatching sprites are shared; everything else has a baby_ version
    const prefix = (s, cfg, name) => /^(egg|hatch)/.test(name) ? "" : stage(s, cfg) === "baby" ? "baby_" : "";

    const statSet = s => s.hatched ? [STATS, s.stats] : [EGG_STATS, s.egg];

    window.PetCore = {
        EGG, STATS, EGG_STATS, clamp, fresh, load, save, ageMs, isBaby, stage, bump, logEvent, tick,
        crackLevel, eggCold, mood, moodInfo, ageText, prefix, statSet
    };
})();

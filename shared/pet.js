// The pet engine: builds the page, runs the care loop, the wardrobe, the minigame, the world and debug mode.
// Everything that makes one pet different from another lives in its config (window.PETS[<body data-pet>]).
(function () {
    const C = window.PETS[document.body.dataset.pet];
    const T = C.text;
    const core = window.PetCore;
    const BASE = (window.SITE_ROOT || "") + C.spriteDir;
    const A = C.activity;

    const $ = id => document.getElementById(id);
    const pick = list => list[Math.floor(Math.random() * list.length)];

    // ---------- page ----------

    document.body.insertAdjacentHTML("afterbegin", `
    <canvas id="world" aria-hidden="true"></canvas>

    <main class="app">
        <header class="top">
            <div class="nameplate">
                <div class="nameline">
                    <a class="back" href="${window.SITE_ROOT || "/"}" aria-label="All pets">‹</a>
                    <h1>${C.name}</h1>
                    <span class="mood" id="mood"></span>
                </div>
                <span class="age" id="age"></span>
            </div>
            <div class="buttons">
                <button class="icon-btn" id="debugBtn" type="button" hidden>Debug</button>
                <button class="icon-btn" id="soundBtn" type="button" aria-pressed="true" aria-label="Sound is on">♪</button>
                <button class="icon-btn" id="closetBtn" type="button">Wardrobe</button>
                <button class="icon-btn" id="diaryBtn" type="button">Diary</button>
            </div>
        </header>

        <section class="stats" id="stats" aria-label="${C.name}'s stats"></section>

        <section class="scene" id="scene">
            <div class="say" id="say" role="status" aria-live="polite"></div>
            <div class="sprite-box" id="spriteBox">
                <img id="pet" src="${BASE}egg_0_1.png" alt="" tabindex="0" draggable="false">
                <img class="acc" id="acc-neck" alt="" hidden>
                <img class="acc" id="acc-face" alt="" hidden>
                <img class="acc" id="acc-head" alt="" hidden>
                ${[0, 1, 2].map(i => `<img class="poop" data-i="${i}" src="${BASE}poop.png" alt="Poop. Tap to clean it up." hidden>`).join("")}
            </div>
            <p class="hint" id="hint"></p>
        </section>

        <nav class="tray" id="tray" aria-label="Things to give ${C.name}">
            ${C.items.map(it => `<button class="item" type="button" data-item="${it.id}"><img src="${BASE}${it.sprite}.png" alt="">${it.label}</button>`).join("")}
            <button class="item" type="button" id="activityBtn"><img src="${BASE}${A.button.sprite}.png" alt="">${A.button.label}</button>
            <button class="item" type="button" id="sleepBtn" aria-pressed="false"><img src="${BASE}moon.png" alt=""><span>Sleep</span></button>
        </nav>
    </main>

    <aside class="sheet diary" id="diary" hidden aria-label="${C.name}'s diary">
        <div class="sheet-head">
            <h2>${C.name}'s diary</h2>
            <button class="icon-btn" type="button" data-close="diary">Close</button>
        </div>
        <ol id="log"></ol>
        <div class="foot" id="counts"></div>
    </aside>

    <aside class="sheet" id="closet" hidden aria-label="${C.name}'s wardrobe">
        <div class="sheet-head">
            <h2>Wardrobe</h2>
            <button class="icon-btn" type="button" data-close="closet">Close</button>
        </div>
        <div class="closet" id="closetGrid"></div>
        <div class="foot">${T.closet.foot}</div>
    </aside>

    <aside class="sheet minigame" id="activity" hidden aria-label="${A.title}">
        <div class="sheet-head">
            <h2>${A.title}</h2>
            <button class="icon-btn" type="button" data-close="activity">Close</button>
        </div>
        <div class="pond ${A.scene}" id="pond"><img id="pondImg" src="${BASE}${A.images.idle}.png" alt=""></div>
        <p class="fish-msg" id="fishMsg" role="status" aria-live="polite"></p>
        <button class="cast-btn" id="castBtn" type="button">${A.text.buttons.start}</button>
    </aside>

    <aside class="debug" id="debug" hidden aria-label="Debug tools">
        <div class="sheet-head">
            <h2>Debug</h2>
            <button class="icon-btn" type="button" data-close="debug">Close</button>
        </div>
        <p class="note">Everything here changes your real saved ${C.name}.</p>
        <section>
            <h3>Stage</h3>
            <div class="row" id="dbgStage">
                <button type="button" data-stage="egg">Egg</button>
                <button type="button" data-stage="baby">${C.stages.babyTitle}</button>
                <button type="button" data-stage="adult">Grown-up</button>
            </div>
        </section>
        <section>
            <h3>Skip time</h3>
            <div class="row">
                <button type="button" data-skip="1">+1 hour</button>
                <button type="button" data-skip="6">+6 hours</button>
                <button type="button" data-skip="24">+1 day</button>
                <button type="button" data-skip="72">+3 days</button>
            </div>
        </section>
        <section>
            <h3>Stats</h3>
            <div id="dbgSliders" style="display: grid; gap: 6px;"></div>
        </section>
        <section>
            <h3>Moods</h3>
            <div class="row">
                ${["Hungry", "Stinky", "Sick", "Sleepy", "Bored", "Overfed", "Perfect"].map(m => `<button type="button" data-mood="${m.toLowerCase()}">${m}</button>`).join("")}
                <button type="button" data-mood="cold">Cold egg</button>
            </div>
        </section>
        <section>
            <h3>Animations</h3>
            <div class="row">
                ${["Eat", "Pet", "Bath", "Play", "Hatch"].map(m => `<button type="button" data-anim="${m.toLowerCase()}">${m}</button>`).join("")}
                <button type="button" data-anim="grow">Grow up</button>
            </div>
        </section>
        <section>
            <h3>Fun stuff</h3>
            <div class="row">
                <button type="button" data-fun="poop">${T.debug.poop}</button>
                <button type="button" data-fun="rare" aria-pressed="false">${A.debugRare}</button>
                <button type="button" data-fun="quick" aria-pressed="false">${A.debugQuick}</button>
                <button type="button" data-fun="star">Shooting star</button>
                <button type="button" data-fun="passer">${C.world.passer.debugLabel}</button>
                <button type="button" data-fun="zoomies">${T.debug.zoomies}</button>
            </div>
        </section>
        <section>
            <h3>Sky</h3>
            <div class="row" id="dbgSky">
                <button type="button" data-sky="">Real time</button>
                ${["dawn", "day", "dusk", "night"].map(p => `<button type="button" data-sky="${p}">${p[0].toUpperCase() + p.slice(1)}</button>`).join("")}
            </div>
        </section>
        <section>
            <h3>Extras</h3>
            <div class="row">
                <button type="button" id="dbgUnlock" aria-pressed="false">Unlock every accessory</button>
                <button type="button" id="dbgWeather" aria-pressed="true">${C.world.weather.label}</button>
            </div>
        </section>
        <section>
            <h3>Start over</h3>
            <div class="row">
                <button type="button" class="danger" id="dbgReset">Reset ${C.name}</button>
            </div>
        </section>
    </aside>`);

    const petEl = $("pet");
    const sceneEl = $("scene");
    const sayEl = $("say");

    // ---------- sprites ----------

    const FRAMES = {
        idle_happy: 2, idle_neutral: 2, idle_hungry: 2, idle_sad: 2, idle_stinky: 2, idle_sleepy: 2,
        idle_sick: 2, idle_overfed: 2, idle_ecstatic: 2, blink: 1, pet: 2, eat: 3, bath: 2, play: 2, sleep: 2,
        egg_0: 2, egg_1: 2, egg_2: 2, egg_cold_0: 2, egg_cold_1: 2, egg_cold_2: 2, hatch: 3
    };
    const SLOTS = ["neck", "face", "head"];

    for (const [name, n] of Object.entries(FRAMES))
        for (const prefix of /^(egg|hatch)/.test(name) ? [""] : ["", "baby_"])
            for (let i = 1; i <= n; i++) new Image().src = `${BASE}${prefix}${name}_${i}.png`;

    // ---------- state ----------

    let { state: S, isNew } = core.load(C);
    let events = { hatched: false, grewUp: false, pooped: false };
    const debug = { sky: "", unlockAll: false, weather: true, rare: false, quick: false };

    const stage = () => core.stage(S, C);
    const isBaby = () => core.isBaby(S, C);
    const save = () => core.save(C, S);
    const bump = (stat, by) => core.bump(S, stat, by);
    const logEvent = msg => core.logEvent(S, msg);
    const count = action => { S.counts[action] = (S.counts[action] || 0) + 1; };
    const spritePath = (name, frame) => `${BASE}${core.prefix(S, C, name)}${name}_${frame + 1}.png`;

    function tick() {
        const e = core.tick(S, C);
        for (const k in e) events[k] ||= e[k];
        save();
    }

    // ---------- sound: tiny chiptune blips, made on the fly ----------

    const SOUNDS = Object.assign({
        chomp: [[220, .06], [180, .06], [240, .08]],
        pet: [[660, .07], [880, .1]],
        egg: [[440, .06, "sine"], [550, .09, "sine"]],
        bubble: [[500, .05, "sine"], [700, .05, "sine"], [900, .07, "sine"]],
        ball: [[392, .07], [523, .07], [659, .1]],
        heal: [[523, .08], [659, .08], [784, .12]],
        hatch: [[523, .1], [659, .1], [784, .1], [1047, .22]],
        grow: [[392, .12], [523, .12], [659, .12], [784, .12], [1047, .3]],
        splash: [[300, .05, "triangle"], [200, .09, "triangle"]],
        bite: [[880, .05], [0, .03], [880, .05]],
        catch: [[659, .08], [784, .08], [988, .16]],
        fail: [[330, .1], [247, .16]],
        poop: [[140, .12, "triangle"], [110, .16, "triangle"]],
        clean: [[700, .05], [1000, .08]],
        wear: [[784, .06], [1175, .1]],
        nope: [[200, .08], [160, .1]],
        zoomies: [[523, .04], [659, .04], [784, .04], [1047, .04], [784, .04], [1047, .04], [1319, .1]]
    }, C.sounds);
    const SFX = Object.assign({ feed: "chomp", pet: "pet", play: "ball", zoomies: "zoomies", start: "splash" }, C.sfx);

    let muted = false;
    try { muted = localStorage.getItem("pets-sound") === "off" || localStorage.getItem("sudo-sound") === "off"; } catch (e) {}
    let audio = null;

    function sfx(name) {
        if (muted || !SOUNDS[name]) return;
        try { audio ||= new AudioContext(); } catch (e) { return; }
        let t = audio.currentTime + 0.01;
        for (const [freq, dur, type = "square"] of SOUNDS[name]) {
            if (freq) {
                const osc = audio.createOscillator(), gain = audio.createGain();
                osc.type = type;
                osc.frequency.value = freq;
                gain.gain.setValueAtTime(0.05, t);
                gain.gain.exponentialRampToValueAtTime(0.001, t + dur);
                osc.connect(gain).connect(audio.destination);
                osc.start(t);
                osc.stop(t + dur);
            }
            t += dur;
        }
    }

    // ---------- rendering ----------

    let anim = null;
    let blinkUntil = 0;

    function animate(name, ms = 1600) { anim = { name, start: Date.now(), until: Date.now() + ms }; }

    const level = v => v < 30 ? "bad" : v < 60 ? "warn" : "good";

    let hudStage = null;

    function renderHud() {
        const [labels, values] = core.statSet(S);
        if (hudStage !== S.hatched) {
            hudStage = S.hatched;
            $("stats").style.setProperty("--cols", Object.keys(labels).length);
            $("stats").innerHTML = Object.entries(labels).map(([k, label]) =>
                `<div class="stat"><div class="stat-head">${label}<b id="v-${k}"></b></div><div class="meter"><i id="m-${k}"></i></div></div>`).join("");
        }
        for (const k of Object.keys(labels)) {
            const v = Math.round(values[k]);
            $("v-" + k).textContent = v;
            const m = $("m-" + k);
            m.style.width = v + "%";
            m.dataset.level = k === "progress" ? "good" : level(v);
        }
        const [text, lvl, hint] = core.moodInfo(S, C);
        $("mood").textContent = text;
        $("mood").dataset.level = lvl;
        $("hint").textContent = hint;
        $("age").textContent = core.ageText(S, C);
        $("tray").classList.toggle("locked", !S.hatched);
        $("sleepBtn").setAttribute("aria-pressed", S.asleep);
        $("sleepBtn").querySelector("span").textContent = S.asleep ? "Wake" : "Sleep";
        petEl.alt = T.alt[stage()];
        if (events.hatched) {
            events.hatched = false;
            animate("hatch", 2400);
            sfx("hatch");
            say(T.hatched, 4500);
            setTimeout(() => burst("sparkle", 5), 1600);
        } else if (events.grewUp) {
            events.grewUp = false;
            sfx("grow");
            say(T.grewUp, 4500);
            burst("sparkle", 5);
        }
        if (events.pooped) {
            events.pooped = false;
            sfx("poop");
            say(T.pooped);
        }
        if (!$("debug").hidden) syncDebug();
    }

    // how far the head has bobbed down in this frame, so accessories follow it
    function headDrop(name, frame) {
        if (name === "eat") return frame === 1 ? 1 : 0;
        if (name === "blink") return 0;
        return frame;
    }

    function renderSprite() {
        const now = Date.now();
        let name, frame;
        if (anim && now < anim.until) {
            name = anim.name;
            // hatching plays once and holds on its last frame; everything else loops
            frame = name === "hatch" ? Math.min(Math.floor((now - anim.start) / 800), 2) : Math.floor((now - anim.start) / 400) % FRAMES[name];
        } else {
            anim = null;
            name = core.mood(S);
            frame = Math.floor(now / 700) % FRAMES[name];
            const canBlink = S.hatched && !["sleep", "idle_overfed", "idle_sick"].includes(name);
            if (canBlink && now > blinkUntil + 2500 && Math.random() < 0.02) blinkUntil = now + 160;
            if (canBlink && now < blinkUntil) { name = "blink"; frame = 0; }
        }
        const src = spritePath(name, frame);
        if (!petEl.src.endsWith(src)) petEl.src = src;

        document.querySelectorAll(".poop").forEach((el, i) => { el.hidden = !S.hatched || i >= S.poops; });

        const showAcc = S.hatched && name !== "hatch";
        const drop = headDrop(name, frame) * world.px;
        for (const slot of SLOTS) {
            const el = $("acc-" + slot);
            const id = S.wearing[slot];
            el.hidden = !showAcc || !id;
            if (el.hidden) continue;
            const accSrc = `${BASE}${core.prefix(S, C, name)}acc_${id}.png`;
            if (!el.src.endsWith(accSrc)) el.src = accSrc;
            el.style.transform = `translateY(${drop}px)`;
        }
    }

    let sayTimer = 0;
    function say(msg, ms = 2600) {
        sayEl.textContent = msg;
        sayEl.classList.add("show");
        clearTimeout(sayTimer);
        sayTimer = setTimeout(() => sayEl.classList.remove("show"), ms);
    }

    // little sprites that float up off the pet
    function burst(sprite, n = 3) {
        const box = petEl.getBoundingClientRect(), scene = sceneEl.getBoundingClientRect();
        for (let i = 0; i < n; i++) {
            const p = document.createElement("img");
            p.src = `${BASE}${sprite}.png`;
            p.className = "particle";
            p.alt = "";
            p.style.left = (box.left - scene.left + box.width * (0.2 + Math.random() * 0.6) - 16) + "px";
            p.style.top = (box.top - scene.top + box.height * (0.15 + Math.random() * 0.35)) + "px";
            p.style.setProperty("--dx", (Math.random() * 60 - 30) + "px");
            p.style.animationDelay = (i * 0.12) + "s";
            sceneEl.appendChild(p);
            setTimeout(() => p.remove(), 1300 + i * 120);
        }
    }

    // ---------- care ----------

    // food goes in, and a few minutes later...
    function digest() { if (!S.nextPoop) S.nextPoop = Date.now() + (3 + Math.random() * 5) * 6e4; }

    const ACTIONS = {
        feed() {
            if (S.asleep) return say(T.feed.asleep);
            if (S.stats.food >= 92) {
                S.overfedUntil = Date.now() + 5 * 6e4;
                bump("fun", -5);
                logEvent(T.feed.fullLog);
                sfx("nope");
                return say(T.feed.full);
            }
            bump("food", 25);
            bump("health", 2);
            count("feed");
            logEvent(T.feed.log);
            digest();
            animate("eat", 1200);
            sfx(SFX.feed);
            say(pick(T.feed.says));
        },

        pet() {
            if (!S.hatched) {
                S.egg.warmth = core.clamp(S.egg.warmth + 12);
                burst("heart", 2);
                sfx("egg");
                return say(pick(T.egg.says));
            }
            count("pet");
            if (S.asleep) { bump("fun", 3); burst("heart", 1); return say(T.pet.asleep); }
            bump("fun", 10);
            logEvent(T.pet.log);
            animate("pet", 1600);
            sfx(SFX.pet);
            burst("heart");
            say(pick(T.pet.says));
        },

        bathe() {
            if (S.asleep) return say(T.bathe.asleep);
            const wasStinky = S.stats.clean < 30;
            S.stats.clean = 100;
            bump("fun", 5);
            count("bathe");
            logEvent(T.bathe.log);
            animate("bath", 2000);
            burst("bubble", 5);
            sfx("bubble");
            say(wasStinky ? T.bathe.stinky : T.bathe.done);
        },

        play() {
            if (S.asleep) return say(T.play.asleep);
            if (S.stats.health < 40) return say(T.play.sick);
            if (S.stats.energy < 15) return say(T.play.tired);
            bump("fun", 20);
            bump("energy", -12);
            bump("food", -5);
            count("play");
            logEvent(T.play.log);
            animate("play", 1600);
            burst("sparkle", 2);
            sfx(SFX.play);
            say(pick(T.play.says));
        },

        heal() {
            if (S.asleep) return say(T.heal.asleep);
            if (S.stats.health >= 70) return say(T.heal.healthy);
            bump("health", 40);
            count("heal");
            logEvent(T.heal.log);
            animate("idle_ecstatic", 1400);
            burst("sparkle", 3);
            sfx("heal");
            say(S.stats.food < 15 || S.stats.clean < 15 ? T.heal.needsMore : T.heal.better);
        },

        sleep() {
            if (S.asleep) {
                S.asleep = false;
                bump("fun", -10);
                logEvent(T.sleep.wokeLog);
                return say(T.sleep.woke);
            }
            if (S.stats.energy > 80) return say(T.sleep.refuse);
            S.asleep = true;
            logEvent(T.sleep.log);
            say(T.sleep.night);
        }
    };

    const ITEM = Object.fromEntries(C.items.map(it => [it.id, it]));

    function cleanPoop() {
        if (!S.poops) return;
        S.poops--;
        bump("fun", 2);
        count("scoop");
        sfx("clean");
        say(pick(T.scoop));
        save();
        renderHud();
    }

    document.querySelectorAll(".poop").forEach(el => el.addEventListener("click", cleanPoop));

    function act(name) {
        tick();
        if (!S.hatched && name !== "pet") { say(T.stillEgg); sfx("nope"); }
        else ACTIONS[name]();
        save();
        renderHud();
    }

    // ---------- dragging items onto the pet ----------

    function overPet(x, y) {
        const r = petEl.getBoundingClientRect();
        const pad = r.width * 0.1;
        return x > r.left - pad && x < r.right + pad && y > r.top - pad && y < r.bottom + pad;
    }

    function makeGhost(sprite, x, y) {
        const g = document.createElement("img");
        g.src = `${BASE}${sprite}.png`;
        g.className = "ghost";
        g.alt = "";
        g.style.left = x + "px";
        g.style.top = y + "px";
        document.body.appendChild(g);
        return g;
    }

    // fly a ghost to a point, then clean up
    function flyTo(g, x, y, done) {
        g.classList.add("fly");
        requestAnimationFrame(() => { g.style.left = x + "px"; g.style.top = y + "px"; });
        setTimeout(() => { g.remove(); done && done(); }, 360);
    }

    function petCenter() {
        const r = petEl.getBoundingClientRect();
        return [r.left + r.width / 2, r.top + r.height * 0.55];
    }

    // tapping (or pressing Enter on) an item tosses it over
    function toss(btn) {
        const it = ITEM[btn.dataset.item];
        const r = btn.getBoundingClientRect();
        const g = makeGhost(it.sprite, r.left + r.width / 2, r.top + r.height / 2);
        const [x, y] = petCenter();
        flyTo(g, x, y, () => act(it.action));
    }

    let drag = null;

    document.querySelectorAll(".item[data-item]").forEach(btn => {
        const it = ITEM[btn.dataset.item];
        btn.addEventListener("pointerdown", e => {
            if (e.button > 0) return;
            e.preventDefault();
            btn.setPointerCapture(e.pointerId);
            drag = { btn, x0: e.clientX, y0: e.clientY, ghost: null, over: false, lastBubble: 0 };
        });

        btn.addEventListener("pointermove", e => {
            if (!drag || drag.btn !== btn) return;
            if (!drag.ghost) {
                if (Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) < 6) return;
                drag.ghost = makeGhost(it.sprite, e.clientX, e.clientY);
                btn.classList.add("dragging");
            }
            drag.ghost.style.left = e.clientX + "px";
            drag.ghost.style.top = e.clientY + "px";
            drag.over = overPet(e.clientX, e.clientY);
            petEl.classList.toggle("target", drag.over);
            // scrubbing with the bath item makes bubbles
            if (drag.over && S.hatched && it.scrub && Date.now() - drag.lastBubble > 220) {
                drag.lastBubble = Date.now();
                burst("bubble", 1);
            }
        });

        const end = e => {
            if (!drag || drag.btn !== btn) return;
            const d = drag;
            drag = null;
            btn.classList.remove("dragging");
            petEl.classList.remove("target");
            if (e.type === "pointercancel") { d.ghost && d.ghost.remove(); return; }
            if (!d.ghost) { toss(btn); return; }
            if (d.over) {
                const [x, y] = petCenter();
                flyTo(d.ghost, x, y, () => act(it.action));
            } else {
                const r = btn.getBoundingClientRect();
                flyTo(d.ghost, r.left + r.width / 2, r.top + r.height / 2);
            }
        };
        btn.addEventListener("pointerup", end);
        btn.addEventListener("pointercancel", end);

        // keyboard: Enter / Space fire a click with no pointer
        btn.addEventListener("click", e => { if (e.detail === 0) toss(btn); });
    });

    $("sleepBtn").addEventListener("click", () => act("sleep"));

    // tap them really fast and they get the zoomies
    let taps = [];
    let zoomUntil = 0;
    function zoomies() {
        zoomUntil = Date.now() + 10000;
        taps = [];
        $("spriteBox").classList.remove("zoomies");
        void $("spriteBox").offsetWidth;
        $("spriteBox").classList.add("zoomies");
        bump("fun", 15);
        bump("energy", -5);
        count("zoomies");
        logEvent(T.zoomies.log);
        sfx(SFX.zoomies);
        say(T.zoomies.say);
        save();
        renderHud();
    }
    $("spriteBox").addEventListener("animationend", () => $("spriteBox").classList.remove("zoomies"));

    petEl.addEventListener("click", () => {
        const now = Date.now();
        taps = taps.filter(t => now - t < 2500).concat(now);
        if (taps.length >= 6 && now > zoomUntil && S.hatched && !S.asleep && S.stats.energy >= 10) return zoomies();
        act("pet");
    });
    petEl.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); act("pet"); } });

    // ---------- sheets ----------

    const SHEETS = ["diary", "closet", "activity", "debug"];

    function openSheet(id, render) {
        for (const other of SHEETS) if (other !== id) $(other).hidden = true;
        render();
        $(id).hidden = false;
        $(id).querySelector("[data-close]").focus();
    }

    document.querySelectorAll("[data-close]").forEach(b => b.addEventListener("click", () => { $(b.dataset.close).hidden = true; }));
    document.addEventListener("keydown", e => { if (e.key === "Escape") for (const id of SHEETS) $(id).hidden = true; });

    $("soundBtn").addEventListener("click", () => {
        muted = !muted;
        try {
            localStorage.setItem("pets-sound", muted ? "off" : "on");
            localStorage.removeItem("sudo-sound");
        } catch (e) {}
        renderSoundBtn();
        sfx("pet");
    });
    function renderSoundBtn() {
        $("soundBtn").textContent = "♪";
        $("soundBtn").setAttribute("aria-pressed", !muted);
        $("soundBtn").setAttribute("aria-label", muted ? "Sound is off" : "Sound is on");
    }
    renderSoundBtn();

    // ---------- diary ----------

    function stamp(t) {
        const d = new Date(t);
        return d.toLocaleString("en-US", { month: "short", day: "2-digit" }) + " " + d.toTimeString().slice(0, 5);
    }

    function untilText(hoursLeft) {
        hoursLeft = Math.max(1, Math.ceil(hoursLeft));
        const days = Math.floor(hoursLeft / 24);
        return `${days ? days + "d " : ""}${hoursLeft % 24}h`;
    }

    function renderDiary() {
        const ol = $("log");
        ol.innerHTML = "";
        for (const e of S.log.slice().reverse()) {
            const li = document.createElement("li");
            const time = document.createElement("time");
            time.textContent = stamp(e.t);
            li.append(time, document.createTextNode(e.msg));
            ol.appendChild(li);
        }
        let status = "";
        if (!S.hatched) status = T.diary.hatchIn(untilText((100 - S.egg.progress) / core.EGG.growth)) + "<br>";
        else if (isBaby()) status = T.diary.growIn(untilText((C.growUpHours * 36e5 - core.ageMs(S)) / 36e5)) + "<br>";
        const tallies = T.diary.counts.map(([k, label]) => `${label}: ${S.counts[k] || 0}`).join(" · ");
        const caught = A.catches.filter(x => S.catches[x.id]).map(x => `${x.short} ${S.catches[x.id]}`).join(" · ");
        $("counts").innerHTML = status + tallies + "<br>" + (caught ? `${A.text.collected}: ${caught}` : A.text.nothingYet);
    }

    $("diaryBtn").addEventListener("click", () => openSheet("diary", renderDiary));

    // ---------- wardrobe ----------

    const unlocked = a => !a.unlock || debug.unlockAll || (a.unlock === "adult" ? stage() === "adult" : S.flags[a.unlock]);

    function renderCloset() {
        const grid = $("closetGrid");
        grid.innerHTML = "";
        if (!S.hatched) {
            grid.innerHTML = `<p class="empty">${T.closet.egg}</p>`;
            return;
        }
        const prefix = stage() === "baby" ? "baby_" : "";
        for (const a of C.accessories) {
            const b = document.createElement("button");
            b.type = "button";
            b.className = "acc-tile";
            b.setAttribute("aria-pressed", S.wearing[a.slot] === a.id);
            b.setAttribute("aria-disabled", !unlocked(a));
            b.innerHTML = `<span class="mini"><img src="${BASE}${prefix}idle_happy_1.png" alt=""><img src="${BASE}${prefix}acc_${a.id}.png" alt=""></span>${a.name}`;
            if (!unlocked(a)) b.insertAdjacentHTML("beforeend", `<small>${a.lockedText}</small>`);
            b.addEventListener("click", () => wear(a));
            grid.appendChild(b);
        }
    }

    function wear(a) {
        if (!unlocked(a)) { sfx("nope"); return say(`${a.name}: ${a.lockedText.toLowerCase()} 🔒`); }
        if (S.wearing[a.slot] === a.id) {
            delete S.wearing[a.slot];
            say(T.closet.takeOff(a.name.toLowerCase()));
        } else {
            S.wearing[a.slot] = a.id;
            logEvent(`put on the ${a.name.toLowerCase()}`);
            say(pick(T.closet.says));
            sfx("wear");
            burst("sparkle", 2);
        }
        save();
        renderCloset();
    }

    $("closetBtn").addEventListener("click", () => openSheet("closet", renderCloset));

    // ---------- the minigame (fishing, snatching...): wait for the moment, then tap fast ----------

    const game = { phase: "idle", timer: 0 };
    const AT = A.text;

    function setPond(phase, img, msg, button) {
        game.phase = phase;
        $("pond").classList.toggle("waiting", phase === "waiting");
        $("pondImg").src = `${BASE}${img}.png`;
        $("pondImg").className = phase === "result" ? "catch" : "";
        $("fishMsg").textContent = msg;
        $("castBtn").textContent = button;
        $("castBtn").classList.toggle("urgent", phase === "bite");
    }

    function resetPond() {
        clearTimeout(game.timer);
        setPond("idle", A.images.idle, AT.intro, AT.buttons.start);
    }

    function pondAction() {
        clearTimeout(game.timer);
        if (game.phase === "waiting") {
            sfx("fail");
            return setPond("idle", A.images.idle, AT.tooEarly, AT.buttons.again);
        }
        if (game.phase === "bite") return grab();
        sfx(SFX.start);
        setPond("waiting", A.images.waiting, AT.waiting, AT.buttons.waiting);
        game.timer = setTimeout(() => {
            sfx("bite");
            setPond("bite", A.images.bite, AT.bite, AT.buttons.bite);
            game.timer = setTimeout(() => {
                sfx("fail");
                setPond("idle", A.images.idle, AT.missed, AT.buttons.again);
            }, 900);
        }, debug.quick ? 300 : 1500 + Math.random() * 3500);
    }

    function roll() {
        const rare = A.catches.find(c => c.rare);
        if (debug.rare) { debug.rare = false; return rare; }
        const total = Object.values(S.catches).reduce((a, b) => a + b, 0);
        // a little bad luck protection for the rare catch
        const table = A.catches.map(c => ({ ...c, weight: c === rare && !S.flags[c.rare] && total >= 15 ? 30 : c.weight }));
        let r = Math.random() * table.reduce((a, c) => a + c.weight, 0);
        return table.find(c => (r -= c.weight) < 0) || table[0];
    }

    // what happens to food once it's caught
    function offerFood(food, fun) {
        if (!S.hatched) return AT.food.egg;
        if (S.asleep) return AT.food.asleep;
        if (S.stats.food >= 92) return AT.food.full;
        bump("food", food);
        bump("fun", fun);
        count("feed");
        digest();
        animate("eat", 1200);
        return AT.food.ate;
    }

    function grab() {
        const c = roll();
        S.catches[c.id] = (S.catches[c.id] || 0) + 1;
        logEvent(AT.log(c.name));
        let msg;
        if (c.food) msg = offerFood(c.food, c.fun || 0);
        else if (c.rare) {
            const first = !S.flags[c.rare];
            S.flags[c.rare] = true;
            if (S.hatched) bump("fun", 30);
            msg = first ? c.firstMsg : c.againMsg;
        } else {
            if (S.hatched) bump("fun", 5);
            msg = c.msg;
        }
        sfx("catch");
        setPond("result", c.sprite || c.id, AT.got(c.name, msg), AT.buttons.again);
        save();
        renderHud();
    }

    $("pond").addEventListener("click", pondAction);
    $("castBtn").addEventListener("click", pondAction);
    $("activityBtn").addEventListener("click", () => openSheet("activity", resetPond));
    document.querySelector('[data-close="activity"]').addEventListener("click", () => clearTimeout(game.timer));

    // ---------- the world: a pixel-art scene behind everything ----------

    const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const canvas = $("world");
    const ctx = canvas.getContext("2d");
    const world = { px: 8, W: 0, H: 0, cx: 0, G: 0, specks: [], passers: [], nextPasser: 8000, star: null };
    const W8 = C.world;

    function phase() {
        if (debug.sky) return debug.sky;
        if (S.hatched && S.asleep) return "night";
        const h = new Date().getHours();
        return h < 5 || h >= 21 ? "night" : h < 8 ? "dawn" : h < 17 ? "day" : "dusk";
    }

    // line the world's pixels up exactly with the pet's pixels
    function layout() {
        const r = $("spriteBox").getBoundingClientRect();
        if (!r.width) return;
        const px = r.width / 32;
        const ox = ((r.left % px) + px) % px - px, oy = ((r.top % px) + px) % px - px;
        world.px = px;
        world.W = Math.ceil((innerWidth - ox) / px) + 1;
        world.H = Math.ceil((innerHeight - oy) / px) + 1;
        canvas.width = world.W;
        canvas.height = world.H;
        Object.assign(canvas.style, { left: ox + "px", top: oy + "px", width: world.W * px + "px", height: world.H * px + "px" });
        world.cx = Math.round((r.left - ox) / px) + 16;
        world.G = Math.round((r.top - oy) / px) + 30;
        const wx = W8.weather;
        const n = Math.round(world.W * world.H / wx.spread);
        world.specks = Array.from({ length: n }, (_, i) => ({
            x: Math.random() * world.W, y: Math.random() * world.H,
            v: wx.speed[0] + Math.random() * (wx.speed[1] - wx.speed[0]), s: i % 7, color: wx.colors[i % wx.colors.length]
        }));
        drawWorld(performance.now());
    }

    const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
    const mix = (a, b, t) => `rgb(${hex(a).map((v, i) => Math.round(v + (hex(b)[i] - v) * t)).join(",")})`;

    function rect(x, y, w, h, color) { ctx.fillStyle = color; ctx.fillRect(x, y, w, h); }

    function disc(cx, cy, r, color) {
        ctx.fillStyle = color;
        for (let y = -r; y <= r; y++) {
            const w = Math.round(Math.sqrt(r * r - y * y));
            ctx.fillRect(cx - w, cy + y, w * 2 + 1, 1);
        }
    }

    // things that pass by in the distance (penguins, ducks...)
    function sendPasser() {
        const p = W8.passer;
        const dir = Math.random() < 0.5 ? 1 : -1;
        const baby = Math.random() < 0.4;
        const speed = p.speed[0] + Math.random() * (p.speed[1] - p.speed[0]);
        world.passers.push({ x: dir > 0 ? -6 : world.W + 6, dir, baby, speed });
        // sometimes little ones tag along behind a grown-up
        if (!baby) for (let i = 1; i <= (Math.random() < p.followChance ? p.followers : 0); i++)
            world.passers.push({ x: dir > 0 ? -6 - i * 7 : world.W + 6 + i * 7, dir, baby: true, speed });
    }

    function drawPasser(w) {
        const p = W8.passer;
        const kind = w.baby ? "baby" : "adult";
        const step = Math.floor(Math.abs(w.x) * 0.8) % 2;
        let rows = p.art[kind].concat(p.feet ? p.feet[kind][step] : []);
        if (p.mirror && w.dir < 0) rows = rows.map(r => [...r].reverse().join(""));
        const top = p.bottom(world.G) - rows.length + 1 - (p.feet ? step : 0);
        rows.forEach((row, y) => [...row].forEach((ch, x) => {
            if (ch !== ".") rect(Math.round(w.x) + x, top + y, 1, 1, p.colors[ch]);
        }));
    }

    const api = { ctx, rect, disc, mix, reduceMotion, world };

    function drawWorld(t) {
        const { W, H, cx, G } = world;
        if (!W) return;
        const ph = phase(), P = W8.phases[ph];
        ctx.clearRect(0, 0, W, H);

        // sky: dithered bands from the top color, through the middle, to the horizon
        const bands = 12;
        const skyAt = f => f < 0.5 ? mix(P.sky[0], P.sky[1], f * 2) : mix(P.sky[1], P.sky[2], (f - 0.5) * 2);
        for (let b = 0; b < bands; b++) {
            const f = b / (bands - 1);
            const y0 = Math.floor(G * b / bands), y1 = Math.floor(G * (b + 1) / bands);
            rect(0, y0, W, y1 - y0, skyAt(f));
            if (b < bands - 1) {
                ctx.fillStyle = skyAt(f + 1 / (bands - 1));
                for (let x = y1 % 2; x < W; x += 2) ctx.fillRect(x, y1 - 1, 1, 1);
            }
        }

        if (ph === "night") {
            for (let i = 0; i < W * 0.6; i++) {
                const x = (i * 73 + 17) % W, y = (i * 151 + 7) % Math.max(1, Math.floor(G * 0.75));
                ctx.globalAlpha = reduceMotion ? 0.8 : 0.45 + 0.55 * Math.abs(Math.sin(t / 900 + i * 1.7));
                rect(x, y, 1, 1, i % 9 === 0 ? "#ffe9a8" : "#ffffff");
            }
            ctx.globalAlpha = 1;
            // crescent moon
            const mx = Math.round(W * 0.8), my = Math.round(G * 0.18);
            disc(mx, my, 5, P.sun);
            disc(mx + 3, my - 2, 4, mix(P.sky[0], P.sky[1], 0.25));
            // shooting stars
            if (!world.star && !reduceMotion && Math.random() < 0.008) world.star = { x: Math.random() * W * 0.7, y: Math.random() * G * 0.3, life: 0 };
            if (world.star) {
                const st = world.star;
                for (let k = 0; k < 6; k++) {
                    ctx.globalAlpha = 1 - k / 6;
                    rect(Math.round(st.x - k * 2), Math.round(st.y - k), 1, 1, "#ffffff");
                }
                ctx.globalAlpha = 1;
                st.x += 2.4; st.y += 1.2;
                if (++st.life > 14) world.star = null;
            }
        } else {
            const low = ph !== "day";
            disc(Math.round(low ? cx - W * 0.28 : W * 0.78), Math.round(low ? G - 10 : G * 0.22), low ? 7 : 4, P.sun);
            // clouds drifting
            for (let i = 0; i < 4; i++) {
                const span = W + 40;
                const x = Math.round(((i * 53 + t / (reduceMotion ? 1e9 : 900) * (0.6 + i * 0.2)) % span) - 20);
                const y = Math.round(G * (0.12 + i * 0.13));
                ctx.globalAlpha = 0.85;
                rect(x, y, 14, 3, P.cloud); rect(x + 3, y - 2, 7, 2, P.cloud); rect(x + 9, y - 1, 4, 1, P.cloud);
                ctx.globalAlpha = 1;
            }
        }

        Object.assign(api, { W, H, cx, G, t, P, phase: ph });
        W8.drawBack(api);

        if (!reduceMotion) {
            if (t > world.nextPasser) { sendPasser(); world.nextPasser = t + 15000 + Math.random() * 25000; }
            for (const w of world.passers) { w.x += w.dir * w.speed; drawPasser(w); }
            world.passers = world.passers.filter(w => w.x > -40 && w.x < W + 40);
        }

        W8.drawFront(api);

        // snow, leaves, whatever falls here
        if (debug.weather) {
            const wx = W8.weather;
            ctx.globalAlpha = 0.9;
            for (const f of world.specks) {
                if (!reduceMotion) {
                    f.y += f.v;
                    f.x += Math.sin(t / 1300 + f.s) * wx.sway;
                    if (f.y > H) { f.y = -1; f.x = Math.random() * W; }
                }
                rect(Math.round(f.x), Math.round(f.y), 1, 1, f.color);
            }
            ctx.globalAlpha = 1;
        }
    }

    let lastDraw = 0;
    function loop(t) {
        if (t - lastDraw > (reduceMotion ? 2000 : 90)) { lastDraw = t; drawWorld(t); }
        requestAnimationFrame(loop);
    }

    addEventListener("resize", layout);
    new ResizeObserver(layout).observe($("spriteBox"));
    if (document.fonts) document.fonts.ready.then(layout);

    // ---------- debug (open the page with #debug) ----------

    function syncDebug() {
        const st = stage();
        document.querySelectorAll("#dbgStage button").forEach(b => b.setAttribute("aria-pressed", b.dataset.stage === st));
        document.querySelectorAll("#dbgSky button").forEach(b => b.setAttribute("aria-pressed", b.dataset.sky === debug.sky));
        $("dbgUnlock").setAttribute("aria-pressed", debug.unlockAll);
        $("dbgWeather").setAttribute("aria-pressed", debug.weather);
        document.querySelector('[data-fun="rare"]').setAttribute("aria-pressed", debug.rare);
        document.querySelector('[data-fun="quick"]').setAttribute("aria-pressed", debug.quick);
        const [labels, values] = core.statSet(S);
        const box = $("dbgSliders");
        if (box.dataset.stage !== String(S.hatched)) {
            box.dataset.stage = S.hatched;
            box.innerHTML = Object.entries(labels).map(([k, label]) =>
                `<label class="slider"><span>${label}</span><input type="range" min="0" max="100" data-stat="${k}"><span></span></label>`).join("");
            box.querySelectorAll("input").forEach(inp => inp.addEventListener("input", () => {
                core.statSet(S)[1][inp.dataset.stat] = Number(inp.value);
                save();
                renderHud();
            }));
        }
        box.querySelectorAll("input").forEach(inp => {
            const v = Math.round(values[inp.dataset.stat]);
            if (document.activeElement !== inp) inp.value = v;
            inp.nextElementSibling.textContent = v;
        });
    }

    function debugDo(fn) { fn(); tick(); renderHud(); }

    function setStage(st) {
        const now = Date.now();
        S.asleep = false;
        if (st === "egg") {
            Object.assign(S, { hatched: false, grown: false, laid: now, born: now, egg: { warmth: 70, progress: 0 } });
            logEvent("went back to being an egg (debug) 🥚");
        } else {
            Object.assign(S, { hatched: true, grown: false, born: st === "baby" ? now : now - C.growUpHours * 36e5 - 6e4 });
            S.egg.progress = 100;
        }
    }

    function skip(hours) {
        const ms = hours * 36e5;
        S.last -= ms;
        S.born -= ms;
        S.laid -= ms;
        S.overfedUntil -= ms;
    }

    const DEBUG_MOODS = {
        hungry() { S.stats.food = 10; },
        stinky() { S.stats.clean = 10; },
        sick() { S.stats.health = 20; },
        sleepy() { S.stats.energy = 10; S.asleep = false; },
        bored() { S.stats.fun = 10; },
        overfed() { S.stats.food = 100; S.overfedUntil = Date.now() + 5 * 6e4; },
        perfect() { for (const k of Object.keys(S.stats)) S.stats[k] = 100; S.overfedUntil = 0; S.asleep = false; },
        cold() { if (!S.hatched) S.egg.warmth = 10; else say("That one's for the egg stage 🥚"); }
    };

    const DEBUG_FUN = {
        poop() { if (!S.hatched) return say(T.stillEgg); S.nextPoop = Date.now() - 1; },
        rare() { debug.rare = !debug.rare; },
        quick() { debug.quick = !debug.quick; },
        star() { world.star = { x: world.W * 0.1, y: world.G * 0.1, life: 0 }; if (phase() !== "night") say("Shooting stars only show up at night. Set the sky to Night 🌙"); },
        passer() { if (reduceMotion) return say("Your device asks for reduced motion, so nobody walks by"); sendPasser(); },
        zoomies() { if (!S.hatched) return say(T.stillEgg); zoomies(); }
    };

    document.querySelectorAll("[data-stage]").forEach(b => b.addEventListener("click", () => debugDo(() => setStage(b.dataset.stage))));
    document.querySelectorAll("[data-skip]").forEach(b => b.addEventListener("click", () => debugDo(() => skip(Number(b.dataset.skip)))));
    document.querySelectorAll("[data-mood]").forEach(b => b.addEventListener("click", () => debugDo(DEBUG_MOODS[b.dataset.mood])));
    document.querySelectorAll("[data-sky]").forEach(b => b.addEventListener("click", () => { debug.sky = b.dataset.sky; syncDebug(); drawWorld(performance.now()); }));
    document.querySelectorAll("[data-anim]").forEach(b => b.addEventListener("click", () => {
        const a = b.dataset.anim;
        if (a === "grow") { events.grewUp = true; renderHud(); return; }
        if (a !== "hatch" && !S.hatched) return say(T.stillEgg);
        animate(a, { eat: 1200, pet: 1600, bath: 2000, play: 1600, hatch: 2400 }[a]);
    }));
    document.querySelectorAll("[data-fun]").forEach(b => b.addEventListener("click", () => { DEBUG_FUN[b.dataset.fun](); tick(); renderHud(); }));

    $("dbgUnlock").addEventListener("click", () => { debug.unlockAll = !debug.unlockAll; syncDebug(); });
    $("dbgWeather").addEventListener("click", () => { debug.weather = !debug.weather; syncDebug(); });

    let resetArmed = 0;
    $("dbgReset").addEventListener("click", () => {
        if (Date.now() - resetArmed > 3000) {
            resetArmed = Date.now();
            $("dbgReset").textContent = "Tap again to really reset";
            setTimeout(() => { $("dbgReset").textContent = `Reset ${C.name}`; }, 3000);
            return;
        }
        resetArmed = 0;
        $("dbgReset").textContent = `Reset ${C.name}`;
        S = core.fresh();
        logEvent(T.log.foundEgg);
        save();
        hudStage = null;
        renderHud();
        say(T.freshEgg);
    });

    function checkDebugHash() {
        const on = location.hash === "#debug";
        $("debugBtn").hidden = !on;
        if (!on) $("debug").hidden = true;
    }
    $("debugBtn").addEventListener("click", () => openSheet("debug", syncDebug));
    addEventListener("hashchange", checkDebugHash);
    checkDebugHash();

    // ---------- boot ----------

    tick();
    if (isNew) {
        logEvent(T.log.foundEgg);
        save();
        setTimeout(() => say(T.foundEgg, 5000), 400);
    } else if (!events.hatched && !events.grewUp) {
        setTimeout(() => say(`Welcome back! ${core.moodInfo(S, C)[2]}`, 3500), 400);
    }

    layout();
    renderHud();
    renderSprite();
    requestAnimationFrame(loop);
    setInterval(renderSprite, 100);
    setInterval(() => { tick(); renderHud(); }, 10000);
    document.addEventListener("visibilitychange", () => { if (!document.hidden) { tick(); renderHud(); } });

    // handy for poking at things from the browser console and for tests
    window.pet = { get state() { return S; }, world, debug };
})();

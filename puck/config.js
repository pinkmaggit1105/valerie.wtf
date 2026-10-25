// Puck the goose: everything that makes her her. The engine in shared/pet.js does the rest.
(window.PETS ||= {}).puck = {
    name: "Puck",
    species: "goose",
    blurb: "A goose who lives by the pond in the park. Loves lettuce and her bell. Will steal your sandwich.",
    saveKey: "puck-pet",
    spriteDir: "sprites/puck/",
    growUpHours: 72,
    card: { sky: "#8cc8f4", ground: "#7cc461", line: "#3f86d0" },
    stages: { baby: "gosling", babyTitle: "Gosling" },

    // [chip text, chip level, hint under her]
    moods: {
        sleep:         ["Asleep", "", "Shh. She's asleep. Do not poke the goose."],
        idle_sick:     ["Sick", "bad", "She's sick! Give her medicine, then feed her and clean her."],
        idle_overfed:  ["Too full", "warn", "Too much lettuce. Give her a few minutes to digest."],
        idle_hungry:   ["Starving", "bad", "She's hungry and getting ideas. Drag some lettuce to her."],
        idle_stinky:   ["Muddy", "warn", "She's been in the mud again. Splash her with the watering can."],
        idle_sleepy:   ["Sleepy", "warn", "Even menaces need naps. Tap the moon to put her to bed."],
        idle_sad:      ["Bored", "warn", "She's bored, which is dangerous. Ring her bell, or pet her."],
        idle_ecstatic: ["Peak goose", "good", "She's never been happier. Nobody's sandwich is safe."],
        idle_happy:    ["Happy", "good", "Drag things onto Puck, or tap her to pet her. At your own risk."],
        idle_neutral:  ["Plotting", "", "She's plotting something. Drag things onto Puck, or tap her to pet her."]
    },
    eggMoods: {
        cold:     ["Cold!", "bad", "The egg is freezing! Tap it to warm it up 🥶"],
        wiggling: ["Wiggling", "good", "It's wiggling... and is that a tiny honk? Keep it warm."],
        egg:      ["Egg", "good", "Tap the egg to keep it warm. It hatches when the Hatching bar fills up."]
    },

    // what she can eat. Strawberries and sandwiches come from raiding the picnic or the shop.
    foods: [
        { id: "lettuce", name: "Lettuce", sprite: "lettuce", food: 25, price: 3, log: "ate some lettuce 🥬" },
        { id: "strawberry", name: "Strawberry", sprite: "strawberry", food: 20, fun: 5, price: 4, log: "ate a strawberry 🍓", say: "She eats it in one gulp 🍓" },
        { id: "corn", name: "Corn", sprite: "corn", food: 30, fun: 5, price: 5, log: "ate some corn 🌽", say: "She shucks it herself. Somehow 🌽" },
        { id: "sandwich", name: "Sandwich", sprite: "sandwich", food: 40, fun: 10, price: 8, log: "ate a whole sandwich 🥪", say: "It was someone's lunch. Now it's hers 🥪" },
        { id: "cake", name: "Cake", sprite: "cake", food: 50, fun: 25, price: 15, log: "ate a slice of cake 🎂", say: "She ate the whole slice in one bite 🎂 No regrets" }
    ],
    starterPantry: { lettuce: 5 },

    items: [
        { id: "food", label: "Food", sprite: "lettuce", action: "feed" },
        { id: "can", label: "Splash", sprite: "can", action: "bathe", scrub: true },
        { id: "bell", label: "Bell", sprite: "bell", action: "play" },
        { id: "pill", label: "Meds", sprite: "pill", action: "heal" }
    ],

    accessories: [
        { id: "tophat", name: "Top hat", slot: "head" },
        { id: "bow", name: "Bow", slot: "head" },
        { id: "partyhat", name: "Party hat", slot: "head" },
        { id: "flowers", name: "Flower crown", slot: "head" },
        { id: "crown", name: "Crown", slot: "head", unlock: "adult", lockedText: "Unlocks when she grows up" },
        { id: "sunhat", name: "Sun hat", slot: "head", unlock: "sunhat", lockedText: "Snatch a sun hat to unlock" },
        { id: "shades", name: "Shades", slot: "face" },
        { id: "heartshades", name: "Heart shades", slot: "face" },
        { id: "scarf", name: "Scarf", slot: "neck" },
        { id: "bowtie", name: "Bow tie", slot: "neck" },
        { id: "chef", name: "Chef's hat", slot: "head", price: 30 },
        { id: "monocle", name: "Monocle", slot: "face", price: 35 },
        { id: "pearls", name: "Pearls", slot: "neck", price: 40 },
        { id: "pirate", name: "Pirate hat", slot: "head", price: 45 },
        { id: "wizard", name: "Wizard hat", slot: "head", price: 50 },
        { id: "halo", name: "Halo", slot: "head", price: 60 }
    ],

    // the picnic: wait for the people to look away, then snatch something
    activity: {
        title: "The picnic",
        button: { label: "Snatch!", sprite: "basket" },
        scene: "grass",
        images: { idle: "basket", waiting: "eye_watch", bite: "eye_away" },
        debugRare: "Sun hat next snatch",
        debugQuick: "Instant openings",
        catches: [
            { id: "strawberry", name: "a strawberry", short: "🍓", weight: 50, pantry: "strawberry", coins: 2 },
            { id: "sandwich", name: "a whole sandwich", short: "🥪", weight: 18, pantry: "sandwich", coins: 4 },
            { id: "sunhat", name: "a sun hat", short: "👒", weight: 4, rare: "sunhat", coins: 25,
              firstMsg: "You unlocked the Sun hat in the Wardrobe!! 👒", againMsg: "Another hat. The park is running out of hats 👒" },
            { id: "keys", name: "the groundskeeper's keys", short: "🔑", weight: 12, coins: 3, msg: "Puck jingles them menacingly 🔑" },
            { id: "phone", name: "someone's phone", short: "📱", weight: 8, coins: 3, msg: "Puck drops it straight into the pond 📱💦" },
            { id: "sock", name: "a single sock", short: "🧦", weight: 8, coins: 1, msg: "Puck treasures it forever 🧦" }
        ],
        text: {
            intro: "Sneak up on the picnic. Wait for them to look away, then SNATCH.",
            waiting: "They're watching... 👀 act natural",
            bite: "!!! They looked away !!!",
            tooEarly: "Too early! They saw you. Pretend you're just a normal goose 🪿",
            missed: "They looked back. Mission failed 😤",
            buttons: { start: "Sneak up", waiting: "Snatch", bite: "SNATCH!", again: "Try again" },
            got: (name, msg) => `You snatched ${name}! ${msg}`,
            log: name => `stole ${name} 🧺`,
            collected: "Stolen",
            nothingYet: "Nothing stolen yet. Tap <b>Snatch!</b> to raid the picnic 🧺",
            stored: "Into the stash it goes 🧺"
        }
    },

    sounds: {
        honk: [[233, .1, "sawtooth"], [0, .03], [208, .16, "sawtooth"]],
        rampage: [[233, .08, "sawtooth"], [0, .03], [233, .08, "sawtooth"], [0, .03], [262, .08, "sawtooth"], [0, .03], [208, .2, "sawtooth"]],
        bell: [[1319, .06, "triangle"], [1568, .05, "triangle"], [1319, .14, "triangle"]],
        sneak: [[330, .04, "triangle"], [0, .05], [294, .04, "triangle"]]
    },
    sfx: { play: "bell", zoomies: "rampage", start: "sneak" },

    text: {
        log: {
            foundEgg: "found a goose egg by the pond 🥚",
            hatched: "hatched! 🐣",
            woke: "woke up and immediately honked ☀️",
            pooped: "pooped on the path 💩",
            grewUp: "grew up into a big goose! 🪿"
        },
        eggAge: "still an egg",
        poopHint: "Ew! She pooped on the path. Tap the poop to clean it up 💩",
        alt: {
            egg: "Puck's egg. Tap to keep it warm.",
            baby: "Baby Puck, a fluffy yellow gosling. Tap to pet her.",
            adult: "Puck the goose. Tap to pet her, if you dare."
        },
        foundEgg: "🥚 You found a big goose egg by the pond! Tap it to keep it warm and it'll hatch in a couple of hours.",
        freshEgg: "🥚 Fresh goose egg! Keep it warm.",
        stillEgg: "She's still in her egg! Tap the egg to keep it warm 🥚",
        hatched: "🐣 PUCK HATCHED!! She's a tiny gosling and she already has opinions.",
        grewUp: "✨ Puck grew up!! She's a big goose now. Lock up your sandwiches 🪿",
        pooped: "💩 Puck pooped. On purpose, probably.",
        egg: { says: ["You cuddle the egg 🥚💕", "Something kicks inside 👀", "You hear a tiny honk!", "Warm and cozy 🥚"] },
        feed: {
            asleep: "Shhh, she's asleep 😴",
            full: "She's too full! Now she has a tummy ache 🤢",
            fullLog: "got overfed and now has a tummy ache 🤢",
            log: "ate some lettuce 🥬",
            says: ["Crunch crunch 🥬", "*aggressive munching* 🥬", "She ate it like it owed her money 🥬", "HONK (thank you) 🥬"]
        },
        pet: {
            asleep: "She mutters a sleepy honk 🥹",
            log: "got petted 🥰",
            says: ["She allows it. This time. 🥰", "*soft honk*", "She leans in. You've been chosen 🥰", "She nibbles your sleeve affectionately"]
        },
        bathe: {
            asleep: "You can't splash a sleeping goose. She'll remember.",
            log: "had a splash 💦",
            stinky: "The mud is gone ✨ She shakes it all over you",
            done: "Splish splash! She flaps around happily ✨"
        },
        play: {
            asleep: "She's asleep. Ring the bell later 😴",
            sick: "She's too sick to play 🤒",
            tired: "She's too tired to play 🥱",
            log: "rang her bell 🔔",
            says: ["DING DING DING 🔔", "She rings it and runs off cackling 🔔", "She's obsessed with this bell 🔔"]
        },
        heal: {
            asleep: "Let her sleep first 😴",
            healthy: "She's healthy! No medicine needed 💚",
            log: "took her medicine 💊",
            better: "Brave goose. She feels much better 💊",
            needsMore: "Much better! Now feed her and clean her 💊"
        },
        sleep: {
            wokeLog: "got woken up 😠",
            woke: "She's awake, and she WILL remember this 😠",
            refuse: "She refuses. Geese do not nap on command 😤",
            log: "went to sleep 💤",
            night: "Goodnight, menace 🌙"
        },
        scoop: ["You scooped it up 🧹✨", "Clean path again ✨", "Puck pretends nothing happened"],
        zoomies: { log: "went on a honking rampage 📢", say: "HONK HONK HONK 📢📢📢" },
        closet: {
            foot: "Tap something to put it on her. She can wear one hat, one pair of shades and one neck thing at a time.",
            egg: "She has to hatch before she can play dress-up 🥚",
            takeOff: name => `She takes off the ${name} and honks at it`,
            says: ["Looking sharp 😎", "A very dapper goose", "She's feeling herself ✨", "Menace, but make it fashion 💅"]
        },
        diary: {
            hatchIn: t => `Hatches in about ${t} if you keep her warm 🥚`,
            growIn: t => `Grows up in ${t} 🐣`,
            counts: [["feed", "Lettuce eaten"], ["pet", "Pets"], ["bathe", "Splashes"], ["play", "Bell rings"], ["scoop", "Poops scooped"]]
        },
        debug: { poop: "Make her poop", zoomies: "Honk rampage" },
        pantry: {
            title: "Snack stash",
            short: "snack stash",
            foot: "Tap something to feed it to her, or drag the Food button onto Puck to feed her the next thing in the stash.",
            empty: "The snack stash is empty! Raid the picnic 🧺 or visit the shop",
            emptyLong: "The snack stash is empty 🧺 Go raid the picnic, or buy something nice in the shop."
        }
    },

    // ---------- her world: the pond in the park ----------

    world: {
        phases: {
            dawn:  { sky: ["#3b3f86", "#c97ba6", "#ffc9a3"], treeFar: "#8a7ea8", tree: "#6e7a8e", treeHi: "#9a9cb8", water: "#6c7cc0", waterHi: "#e8b8c8", ground: "#8fb27a", groundHi: "#b4c896", shadow: "#738f62", wood: "#8a5a3a", woodDk: "#5e3c26", blanket: "#d8667a", blanketHi: "#fbe8ea", lamp: "#3a3f52", lit: false, sun: "#ffb36b", cloud: "#fbe3ea" },
            day:   { sky: ["#4fa3e8", "#8cc8f4", "#d8f0ff"], treeFar: "#6fae7a", tree: "#4f9a5c", treeHi: "#7cc486", water: "#3f86d0", waterHi: "#a6d6fa", ground: "#7cc461", groundHi: "#9ad97a", shadow: "#5ea64a", wood: "#9a6236", woodDk: "#6e4222", blanket: "#e0525e", blanketHi: "#fff3ea", lamp: "#3a3f52", lit: false, sun: "#fff2a8", cloud: "#ffffff" },
            dusk:  { sky: ["#2a2f6e", "#a2508a", "#f59a6a"], treeFar: "#5b4a7e", tree: "#4c4a6a", treeHi: "#6e6a8e", water: "#4b4a9a", waterHi: "#f2a88a", ground: "#6e8a5e", groundHi: "#8aa070", shadow: "#56704a", wood: "#7a4e34", woodDk: "#523422", blanket: "#c24c5e", blanketHi: "#f4d8d8", lamp: "#2e3246", lit: true, sun: "#ff8a5c", cloud: "#f6c4c4" },
            night: { sky: ["#070a24", "#121a4a", "#263a7a"], treeFar: "#17244a", tree: "#13203e", treeHi: "#24345e", water: "#13235a", waterHi: "#4c5f9c", ground: "#2e4a3e", groundHi: "#3e5e4c", shadow: "#22382e", wood: "#4a3428", woodDk: "#2e2018", blanket: "#7a3442", blanketHi: "#9a8c9a", lamp: "#262a3e", lit: true, sun: "#f4f1d0", cloud: "#33407a" }
        },

        weather: { label: "Leaves", colors: ["#f2a541", "#e0703a", "#f6d06b", "#c95a3a"], spread: 420, speed: [0.08, 0.18], sway: 0.25 },

        // ducks paddling across the pond, often with a row of ducklings. G green head, Y beak, B body, D duckling, O duckling beak
        passer: {
            debugLabel: "Send ducks",
            art: {
                adult: ["....GG.", "....GGY", "BBBBBB.", ".BBBB.."],
                baby: ["..DD.", "..DDO", "DDDD."]
            },
            feet: null,
            mirror: true,
            colors: { G: "#2f7a4a", Y: "#f2b632", B: "#8a6a4a", D: "#f6d860", O: "#f2913a" },
            bottom: G => G - 2,
            speed: [0.08, 0.14],
            followChance: 0.7,
            followers: 3
        },

        // behind the ducks: trees across the water, then the pond itself
        drawBack({ rect, W, cx, G, t, P, reduceMotion }) {
            const shore = G - 6;
            for (let x = 0; x < W; x++) {
                const wx = x - cx;
                const hf = Math.round(15 + 3 * Math.sin(wx * 0.21 + 1) + 2 * Math.sin(wx * 0.47) + 3 * Math.abs(Math.sin(wx * 0.13)));
                rect(x, shore - hf, 1, hf, P.treeFar);
                const hn = Math.round(8 + 3 * Math.sin(wx * 0.17 + 2) + 2 * Math.sin(wx * 0.39 + 0.5));
                rect(x, shore - hn, 1, hn, P.tree);
                rect(x, shore - hn, 1, 1, P.treeHi);
            }
            rect(0, shore, W, G - shore, P.water);
            const drift = reduceMotion ? 0 : Math.floor(t / 500);
            for (let x = 0; x < W; x++)
                if ((x + drift) % 9 === 0) rect(x, shore + 1 + (x * 7) % 4, 2, 1, P.waterHi);
        },

        // in front: the grass, a bench, a picnic blanket, a lamp post, flowers and fireflies
        drawFront({ ctx, rect, disc, W, H, cx, G, t, P, phase, reduceMotion }) {
            rect(0, G, W, H - G, P.ground);
            rect(0, G, W, 1, P.groundHi);
            for (let i = 0; i < W * 1.5; i++) {
                const x = (i * 97 + 31) % W, y = G + 2 + (i * 41) % Math.max(1, H - G - 2);
                rect(x, y, 1, 2, P.shadow);
            }
            const petals = ["#ffd1e0", "#fff2a8", "#ffffff"];
            for (let i = 0; i < W * 0.4; i++) {
                const x = (i * 53 + 11) % W, y = G + 2 + (i * 29) % Math.max(1, H - G - 2);
                if (Math.abs(x - cx) > 12) rect(x, y, 1, 1, petals[i % 3]);
            }
            rect(cx - 11, G, 22, 1, P.shadow);
            rect(cx - 8, G + 1, 16, 1, P.shadow);

            // a park bench to her left
            const bx = cx - 34;
            for (const y of [G - 11, G - 9]) rect(bx - 8, y, 17, 1, P.wood);
            rect(bx - 7, G - 11, 1, 6, P.woodDk); rect(bx + 7, G - 11, 1, 6, P.woodDk);
            rect(bx - 9, G - 6, 19, 1, P.wood);
            rect(bx - 9, G - 5, 19, 1, P.woodDk);
            rect(bx - 7, G - 4, 1, 4, P.woodDk); rect(bx + 7, G - 4, 1, 4, P.woodDk);

            // somebody's picnic to her right (the one she keeps raiding)
            const px = cx + 30;
            for (let y = 0; y < 5; y++)
                for (let x = -9; x <= 9; x++)
                    rect(px + x + y, G + 1 + y, 1, 1, (Math.floor((x + 9) / 3) + y) % 2 ? P.blanket : P.blanketHi);
            rect(px - 2, G - 2, 7, 4, "#d9a860");
            rect(px - 2, G - 2, 7, 1, "#b07c40");
            rect(px - 1, G - 5, 1, 3, "#b07c40"); rect(px + 3, G - 5, 1, 3, "#b07c40"); rect(px, G - 5, 3, 1, "#b07c40");

            // a lamp post that switches on in the evening
            const lx = cx + 52;
            if (P.lit) {
                ctx.globalAlpha = 0.22;
                disc(lx, G - 22, 7, "#ffe9a0");
                ctx.globalAlpha = 1;
            }
            rect(lx, G - 20, 1, 20, P.lamp);
            rect(lx - 1, G - 1, 3, 1, P.lamp);
            rect(lx - 2, G - 24, 5, 1, P.lamp);
            rect(lx - 1, G - 23, 3, 2, P.lit ? "#fff4b8" : "#c8ccd8");

            // fireflies
            if (phase === "night") {
                for (let i = 0; i < 14; i++) {
                    const x = Math.round((i * 61 + 7) % W + Math.sin(t / 2100 + i) * 5);
                    const y = Math.round(G - 3 - (i * 13) % 16 + Math.cos(t / 1700 + i * 2) * 2);
                    ctx.globalAlpha = reduceMotion ? 0.8 : Math.max(0.15, Math.sin(t / 420 + i * 1.3));
                    rect(x, y, 1, 1, "#e8ff7a");
                }
                ctx.globalAlpha = 1;
            }
        }
    }
};

// Sudo the penguin: everything that makes him him. The engine in shared/pet.js does the rest.
(window.PETS ||= {}).sudo = {
    name: "Sudo",
    species: "penguin",
    blurb: "A tiny Tux-ish penguin who lives on the ice next to his igloo. Loves fish, hates being woken up.",
    saveKey: "sudo-pet",
    spriteDir: "sprites/sudo/",
    growUpHours: 72,
    card: { sky: "#79b9f2", ground: "#eef6ff", line: "#bcd0ea" },
    stages: { baby: "baby", babyTitle: "Baby" },

    // [chip text, chip level, hint under him]
    moods: {
        sleep:         ["Asleep", "", "Shh, he's sleeping. He wakes up by himself once he's rested."],
        idle_sick:     ["Sick", "bad", "He's sick! Give him medicine, then feed him and clean him."],
        idle_overfed:  ["Too full", "warn", "Too many fish. Give his tummy a few minutes."],
        idle_hungry:   ["Starving", "bad", "He's hungry. Drag a fish to him."],
        idle_stinky:   ["Stinky", "warn", "Phew. Scrub him with the soap."],
        idle_sleepy:   ["Sleepy", "warn", "He can barely keep his eyes open. Tap the moon to put him to bed."],
        idle_sad:      ["Bored", "warn", "He's bored. Throw him the ball, or pet him."],
        idle_ecstatic: ["Best life", "good", "He's never been happier."],
        idle_happy:    ["Happy", "good", "Drag things onto Sudo, or tap him to pet him."],
        idle_neutral:  ["Okay", "", "Drag things onto Sudo, or tap him to pet him."]
    },
    eggMoods: {
        cold:     ["Cold!", "bad", "The egg is freezing! Tap it to warm it up 🥶"],
        wiggling: ["Wiggling", "good", "It's wiggling... almost there! Keep it warm."],
        egg:      ["Egg", "good", "Tap the egg to keep it warm. It hatches when the Hatching bar fills up."]
    },

    // what he can eat. Fish come from fishing or the shop; the rest only from the shop.
    foods: [
        { id: "fish", name: "Fish", sprite: "fish", food: 25, price: 3, log: "ate a fish 🐟" },
        { id: "bigfish", name: "Big fish", sprite: "bigfish", food: 40, fun: 5, price: 6, log: "ate a big fish 🐠", say: "A BIG one!! He's thrilled 🐠" },
        { id: "icecream", name: "Ice cream", sprite: "icecream", food: 15, fun: 25, price: 8, log: "had some ice cream 🍦", say: "Brain freeze!! 🍦 He loves it" },
        { id: "taco", name: "Fish taco", sprite: "taco", food: 35, fun: 15, price: 10, log: "ate a fish taco 🌮", say: "A fish TACO?? Best day of his life 🌮" },
        { id: "sushi", name: "Sushi platter", sprite: "sushi", food: 55, fun: 20, price: 15, log: "ate a whole sushi platter 🍣", say: "Fancy!! He eats it very politely 🍣" }
    ],
    starterPantry: { fish: 5 },

    items: [
        { id: "food", label: "Food", sprite: "fish", action: "feed" },
        { id: "soap", label: "Soap", sprite: "soap", action: "bathe", scrub: true },
        { id: "ball", label: "Ball", sprite: "ball", action: "play" },
        { id: "pill", label: "Meds", sprite: "pill", action: "heal" }
    ],

    accessories: [
        { id: "tophat", name: "Top hat", slot: "head" },
        { id: "beanie", name: "Beanie", slot: "head" },
        { id: "bow", name: "Bow", slot: "head" },
        { id: "crown", name: "Crown", slot: "head", unlock: "adult", lockedText: "Unlocks when he grows up" },
        { id: "shades", name: "Shades", slot: "face" },
        { id: "scarf", name: "Scarf", slot: "neck" },
        { id: "partyhat", name: "Party hat", slot: "head" },
        { id: "flowers", name: "Flower crown", slot: "head" },
        { id: "headphones", name: "Headphones", slot: "head" },
        { id: "heartshades", name: "Heart shades", slot: "face" },
        { id: "bowtie", name: "Bow tie", slot: "neck" },
        { id: "fishhat", name: "Fish hat", slot: "head", unlock: "golden", lockedText: "Catch a golden fish to unlock" },
        { id: "chef", name: "Chef's hat", slot: "head", price: 30 },
        { id: "monocle", name: "Monocle", slot: "face", price: 35 },
        { id: "pearls", name: "Pearls", slot: "neck", price: 40 },
        { id: "pirate", name: "Pirate hat", slot: "head", price: 45 },
        { id: "wizard", name: "Wizard hat", slot: "head", price: 50 },
        { id: "halo", name: "Halo", slot: "head", price: 60 }
    ],

    activity: {
        title: "Fishing hole",
        button: { label: "Fish!", sprite: "rod" },
        scene: "",
        images: { idle: "rod", waiting: "bobber", bite: "bobber_dip" },
        debugRare: "Golden fish next cast",
        debugQuick: "Instant bites",
        catches: [
            { id: "fish", name: "a fish", short: "🐟", weight: 55, pantry: "fish", coins: 2 },
            { id: "bigfish", name: "a BIG fish", short: "big 🐠", weight: 18, pantry: "bigfish", coins: 4 },
            { id: "goldfish", name: "a GOLDEN fish", short: "golden ✨", weight: 4, rare: "golden", coins: 25,
              firstMsg: "You unlocked the Fish hat in the Wardrobe!! 🎩🐟", againMsg: "Another one! Sudo is in awe ✨" },
            { id: "boot", name: "an old boot", short: "👢", weight: 10, coins: 1, msg: "Sudo stares at it, very confused 👢" },
            { id: "seaweed", name: "some seaweed", short: "🌿", weight: 8, coins: 1, msg: "Sudo wears it like a wig for a second 🌿" },
            { id: "icecube", name: "an ice cube", short: "🧊", weight: 5, coins: 1, msg: "It's just ice. Sudo licks it anyway 🧊" }
        ],
        text: {
            intro: "Tap Cast, wait for a bite, then reel it in FAST.",
            waiting: "Waiting for a bite...",
            bite: "!!! Something's biting !!!",
            tooEarly: "Too early! You scared it off 🐟💨",
            missed: "It got away... 🐟💨 Be quicker next time!",
            buttons: { start: "Cast", waiting: "Reel in", bite: "REEL IN!", again: "Cast again" },
            got: (name, msg) => `You caught ${name}! ${msg}`,
            log: name => `caught ${name} 🎣`,
            collected: "Caught",
            nothingYet: "Nothing caught yet. Tap <b>Fish!</b> to go fishing 🎣",
            stored: "Into the bucket it goes 🪣"
        }
    },

    text: {
        log: {
            foundEgg: "found an egg 🥚",
            hatched: "hatched! 🐣",
            woke: "woke up all on his own ☀️",
            pooped: "pooped 💩",
            grewUp: "grew up into a big penguin! 🐧"
        },
        eggAge: "still an egg",
        poopHint: "Ew! He pooped. Tap the poop to clean it up 💩",
        alt: {
            egg: "Sudo's egg. Tap to keep it warm.",
            baby: "Baby Sudo, a fluffy penguin chick. Tap to pet him.",
            adult: "Sudo the penguin. Tap to pet him."
        },
        foundEgg: "🥚 You found an egg! Tap it to keep it warm and it'll hatch in a couple of hours.",
        freshEgg: "🥚 Fresh egg! Keep it warm.",
        stillEgg: "He's still in his egg! Tap the egg to keep it warm 🥚",
        hatched: "🐣 SUDO HATCHED!! Say hi to your baby!",
        grewUp: "✨ Sudo grew up!! He's a big penguin now 🐧",
        pooped: "💩 Oops. Sudo pooped.",
        egg: { says: ["You cuddle the egg 🥚💕", "Something wiggles inside 👀", "Warm and cozy 🥚", "You hear a tiny peep!"] },
        feed: {
            asleep: "Shhh, he's sleeping 😴",
            full: "He's too full! Now he has a tummy ache 🤢",
            fullLog: "got force-fed and now has a tummy ache 🤢",
            log: "ate a fish 🐟",
            says: ["Nom nom nom 🐟", "*gulp* 🐟", "Fish! His favorite! 🐟", "He ate it in one bite 🐟"]
        },
        pet: {
            asleep: "He smiles in his sleep 🥹",
            log: "got petted 🥰",
            says: ["*happy wiggle*", "He leans into your hand 🥰", "*happy penguin noises*", "He's blushing. He's shy."]
        },
        bathe: {
            asleep: "You can't bathe a sleeping penguin 😭",
            log: "had a bath 🫧",
            stinky: "FINALLY. The fly has left ✨",
            done: "Splish splash! Squeaky clean ✨"
        },
        play: {
            asleep: "He's asleep. Play later 😴",
            sick: "He's too sick to play 🤒",
            tired: "He's too tired to play 🥱",
            log: "played ball 🎾",
            says: ["He bonked it with his head! 🎾", "BALL!!! 🎾", "He's thrilled 🎾"]
        },
        heal: {
            asleep: "Let him sleep first 😴",
            healthy: "He's healthy! No medicine needed 💚",
            log: "took his medicine 💊",
            better: "Brave little guy. He feels much better 💊",
            needsMore: "Much better! Now feed him and clean him 💊"
        },
        sleep: {
            wokeLog: "got woken up 😠",
            woke: "He's awake, and grumpy about it 😠",
            refuse: "He refuses. He is NOT tired 😤",
            log: "went to sleep 💤",
            night: "Goodnight, little guy 🌙"
        },
        scoop: ["You scooped it up 🧹✨", "Clean ice again ✨", "Sudo looks relieved 😌"],
        zoomies: { log: "got the zoomies 🌀", say: "Zoomies!!! 🌀🌀🌀" },
        closet: {
            foot: "Tap something to put it on him. He can wear one hat, one pair of shades and one scarf at a time.",
            egg: "He has to hatch before he can play dress-up 🥚",
            takeOff: name => `He takes off the ${name}`,
            says: ["Looking sharp 😎", "So stylish!!", "He's feeling himself ✨", "A fashion icon 💅"]
        },
        diary: {
            hatchIn: t => `Hatches in about ${t} if you keep him warm 🥚`,
            growIn: t => `Grows up in ${t} 🐣`,
            counts: [["feed", "Fish eaten"], ["pet", "Pets"], ["bathe", "Baths"], ["play", "Ball games"], ["scoop", "Poops scooped"]]
        },
        debug: { poop: "Make him poop", zoomies: "Zoomies" },
        pantry: {
            title: "Fish bucket",
            short: "fish bucket",
            foot: "Tap something to feed it to him, or drag the Food button onto Sudo to feed him the next thing in the bucket.",
            empty: "The fish bucket is empty! Go fishing 🎣 or visit the shop",
            emptyLong: "The fish bucket is empty 🪣 Go catch some fish, or buy something nice in the shop."
        }
    },

    // ---------- his world: the ice outside his igloo ----------

    world: {
        phases: {
            dawn:  { sky: ["#3b3f86", "#c97ba6", "#ffc9a3"], far: "#8d86c0", farCap: "#e9d9f0", near: "#b7b2dd", nearCap: "#fbeef6", ground: "#f6eef4", groundHi: "#ffffff", shadow: "#d6c8de", igloo: "#fbf6fb", iglooLine: "#d2c1d8", door: "#4a3f78", water: "#3e4f9a", waterHi: "#8aa0dc", sun: "#ffb36b", cloud: "#fbe3ea" },
            day:   { sky: ["#3f8fe0", "#79b9f2", "#cfe8ff"], far: "#8fb4e3", farCap: "#eef6ff", near: "#b4d0f0", nearCap: "#ffffff", ground: "#eef6ff", groundHi: "#ffffff", shadow: "#c3d7f0", igloo: "#f7fbff", iglooLine: "#bcd0ea", door: "#33437a", water: "#2f6fc0", waterHi: "#8cc4f5", sun: "#fff2a8", cloud: "#ffffff" },
            dusk:  { sky: ["#2a2f6e", "#a2508a", "#f59a6a"], far: "#6b4f8e", farCap: "#e5b7c8", near: "#8f6aa6", nearCap: "#f2cbd8", ground: "#e9d3e0", groundHi: "#f8e8f0", shadow: "#c3a3bd", igloo: "#f2e2ec", iglooLine: "#c29fb8", door: "#3a2c5e", water: "#3a3f88", waterHi: "#9b8acb", sun: "#ff8a5c", cloud: "#f6c4c4" },
            night: { sky: ["#070a24", "#121a4a", "#263a7a"], far: "#1d2754", farCap: "#5a6aa0", near: "#28366a", nearCap: "#7b8cc2", ground: "#9fb2dc", groundHi: "#c6d3f0", shadow: "#7a8dbf", igloo: "#aebfe4", iglooLine: "#7f93c4", door: "#f7c14e", water: "#0e1846", waterHi: "#4c5f9c", sun: "#f4f1d0", cloud: "#33407a" }
        },

        weather: { label: "Snow", colors: ["#ffffff"], spread: 140, speed: [0.15, 0.4], sway: 0.08 },

        // little penguins that waddle past in the distance. B black, W white, Y beak and feet, G baby fluff
        passer: {
            debugLabel: "Send a penguin",
            art: {
                adult: [".BBB.", "BWBWB", "BBYBB", "BWWWB", "BWWWB", "BWWWB"],
                baby: [".BB.", "BWWB", "GYYG", "GGGG"]
            },
            feet: { adult: ["Y...Y", ".Y.Y."], baby: ["Y..Y", ".YY."] },
            colors: { B: "#22232e", W: "#f4f4f0", Y: "#fcc436", G: "#969cac" },
            bottom: G => G - 1,
            speed: [0.12, 0.2],
            followChance: 0.5,
            followers: 1
        },

        // behind the passers: the aurora, mountains and icebergs
        drawBack({ ctx, rect, W, cx, G, t, P, phase }) {
            if (phase === "night") {
                for (let x = 0; x < W; x++) {
                    const wx = x - cx;
                    const y = Math.round(G * 0.2 + Math.sin(wx * 0.11 + t / 2400) * 3 + Math.sin(wx * 0.043 - t / 3300) * 5);
                    for (let k = 0; k < 9; k++) {
                        ctx.globalAlpha = 0.32 * (1 - k / 9);
                        rect(x, y + k, 1, 1, k < 3 ? "#7df5c4" : "#4fd1a0");
                    }
                    ctx.globalAlpha = 0.18;
                    rect(x, y - 3, 1, 3, "#8a7cf0");
                }
                ctx.globalAlpha = 1;
            }
            // heights come from Sudo's position so they don't jump around
            for (let x = 0; x < W; x++) {
                const wx = x - cx;
                const hf = Math.round(16 + 6 * Math.sin(wx * 0.09 + 1.3) + 4 * Math.sin(wx * 0.23 + 0.4) + 2 * Math.sin(wx * 0.51));
                rect(x, G - hf, 1, hf, P.far);
                rect(x, G - hf, 1, hf > 18 ? 3 : 1, P.farCap);
                const hn = Math.round(6 + 3 * Math.sin(wx * 0.13 + 2) + 2 * Math.sin(wx * 0.31 + 1));
                rect(x, G - hn, 1, hn, P.near);
                rect(x, G - hn, 1, 1, P.nearCap);
            }
        },

        // in front: the ice, his igloo, the fishing hole and a snowman
        drawFront({ rect, disc, W, H, cx, G, t, P, reduceMotion }) {
            rect(0, G, W, H - G, P.ground);
            rect(0, G, W, 1, P.groundHi);
            for (let i = 0; i < W * 1.5; i++) {
                const x = (i * 97 + 31) % W, y = G + 3 + (i * 41) % Math.max(1, H - G - 3);
                rect(x, y, 2, 1, P.shadow);
            }
            rect(cx - 11, G, 22, 1, P.shadow);
            rect(cx - 8, G + 1, 16, 1, P.shadow);

            // igloo to his left, door facing him (it glows at night)
            const ix = cx - 36;
            for (let y = -11; y <= 0; y++) {
                for (let x = -13; x <= 13; x++) {
                    if ((x / 13) ** 2 + (y / 11.5) ** 2 > 1) continue;
                    const edge = (x / 13) ** 2 + (y / 11.5) ** 2 > 0.82;
                    const brick = y % 4 === 0 || (x + (Math.floor(y / 4) % 2 ? 3 : 0)) % 6 === 0;
                    rect(ix + x, G + y, 1, 1, edge || brick ? P.iglooLine : P.igloo);
                }
            }
            for (let y = -6; y <= 0; y++)
                for (let x = 6; x <= 12; x++)
                    if (((x - 9) / 3.4) ** 2 + (y / 6.5) ** 2 <= 1) rect(ix + x, G + y, 1, 1, P.door);

            // fishing hole to his right
            const fx = cx + 27, fy = G + 2;
            for (let y = -2; y <= 2; y++) {
                const w = Math.round(8 * Math.sqrt(1 - (y / 2.6) ** 2));
                rect(fx - w, fy + y, w * 2 + 1, 1, y === -2 ? P.shadow : P.water);
            }
            const ripple = reduceMotion ? 0 : Math.floor(t / 600) % 4;
            rect(fx - 3 + ripple, fy, 3, 1, P.waterHi);

            // a snowman keeping him company, past the fishing hole
            const sx = cx + 46;
            disc(sx, G - 4, 4, P.iglooLine); disc(sx - 1, G - 4, 4, P.igloo);
            disc(sx, G - 10, 3, P.iglooLine); disc(sx - 1, G - 10, 3, P.igloo);
            disc(sx, G - 15, 2, P.iglooLine); disc(sx - 1, G - 15, 2, P.igloo);
            rect(sx - 2, G - 16, 1, 1, "#22232e"); rect(sx, G - 16, 1, 1, "#22232e");
            rect(sx - 1, G - 15, 2, 1, "#f08a24");
            rect(sx - 3, G - 18, 5, 1, "#22232e"); rect(sx - 2, G - 21, 3, 3, "#22232e");
            for (let i = 0; i < 4; i++) { rect(sx - 4 - i, G - 11 - i, 1, 1, "#8c5834"); rect(sx + 3 + i, G - 11 - i, 1, 1, "#8c5834"); }
        }
    }
};

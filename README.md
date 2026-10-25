# valerie.wtf

Sudo is a tiny pixel penguin who lives at valerie.wtf. Hatch his egg, then look after him: drag fish to him, scrub him with soap, take him fishing, dress him up, clean up after him, and don't let him get sick 🐧

**Live at [valerie.wtf](https://valerie.wtf)**

## Growing up

1. 🥚 **Egg.** Tap the egg to keep it warm. It cools off over time, and it only grows while it's warm (it shivers and turns blue when it's cold). After about 2½ warm hours it cracks open
2. 🐣 **Baby.** A fluffy grey chick for his first 3 days
3. 🐧 **Grown-up.** A big Tux-ish penguin with his own little curl of a tuft

## Looking after Sudo

Drag an item from the tray onto Sudo, or just tap it and it flies over to him:

| Item | What it does |
| --- | --- |
| 🐟 Fish | Feeds him. Feed him when he's already full and he gets a tummy ache 🤢 |
| 🧼 Soap | Bath time. Scrub him with it and bubbles come off |
| 🎾 Ball | Play. Makes him happy, but uses up energy and food |
| 💊 Meds | Only does anything when he's sick |
| 🎣 Fish! | Go fishing (see below) |
| 🌙 Sleep | Puts him to bed, or wakes him up (he's grumpy about it). He won't go to bed if he isn't tired |

Tap Sudo himself to pet him 🥰

His food, fun, cleanliness and energy go down over time, even while the tab is closed, so come back and check on him. A full tummy lasts about half a day. If he's left hungry or stinky for too long he gets sick 🤒. The **Diary** button shows everything that's happened to him, plus everything you've caught.

A few minutes after he eats, he poops 💩. Tap it to clean it up. Poop left lying around makes him dirty, and a lot of it makes him ill.

### Fishing 🎣

Tap **Fish!**, cast your line, wait for the bobber to dip, then reel in fast. Too early and you scare the fish off, too late and it gets away. You might catch a fish or a big fish (Sudo eats them if he's hungry), an old boot, seaweed, an ice cube, or, very rarely, a **golden fish**, which unlocks the fish hat.

### Wardrobe 🎩

Twelve accessories, each in a baby size and a grown-up size: a top hat, beanie, bow, party hat, flower crown, headphones, shades, heart shades, scarf and bow tie, plus a crown (unlocks when he grows up) and a fish hat (catch a golden fish). He can wear one hat, one pair of shades and one neck thing at once.

### His world

He lives on the ice outside his igloo, next to a fishing hole and a snowman, with mountains behind him and other penguins waddling past now and then. The sky follows your clock: dawn, day, dusk, and night with stars, shooting stars, an aurora, and a glowing igloo door. It's always night while he sleeps.

Every action has a little chiptune sound. The ♪ button turns them off. There are a few secrets too 👀

For now Sudo lives in your browser (`localStorage`), so everyone has their own Sudo. A shared version where everyone raises one Sudo together is the plan for later.

### Debug mode 🐞

Add `#debug` to the address ([valerie.wtf/#debug](https://valerie.wtf/#debug)) and a **Debug** button appears. It can switch stages, skip time, set any stat, trigger moods and animations, make him poop, rig the next catch to be golden, make fish bite instantly, send a shooting star or a passing penguin, change the sky, unlock every accessory, turn snow off, and reset Sudo back to an egg. It changes your real saved Sudo.

## How it's built

It's a single HTML file with plain HTML, CSS and JavaScript: no frameworks, no build step, no dependencies. It's hosted on GitHub Pages with the custom domain set in `CNAME`.

- `index.html`: Sudo. The world behind him is drawn on a canvas whose pixels line up with his
- `sprites/`: the 32×32 pixel-art sprites (`baby_*` for baby Sudo, `egg_*` and `hatch_*` for the egg, `acc_*` for accessories) and the 16×16 items. They're drawn by `tools/make_sprites.py` (needs Pillow: `python3 tools/make_sprites.py sprites preview.png`), so a new sprite is a few lines of Python
- `archive/`: older versions of the site. valerie.wtf used to be a terminal for learning Linux package managers (`terminal-v1.html`, `terminal-v2.html`) with a typing game called Package Panic (`package-panic-v1.html`)

To run it locally, open `index.html` in a browser.

## Contact

valeriecollins05(at)proton(dot)me

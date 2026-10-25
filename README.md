# valerie.wtf

Sudo is a tiny pixel penguin who lives at valerie.wtf. Hatch his egg, then look after him: drag fish to him, scrub him with soap, throw him a ball, dress him up, and don't let him get sick 🐧

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
| 💊 Medicine | Only does anything when he's sick |
| 🌙 Moon | Puts him to bed, or wakes him up (he's grumpy about it). He won't go to bed if he isn't tired |

Tap Sudo himself to pet him 🥰

His food, fun, cleanliness and energy go down over time, even while the tab is closed, so come back and check on him. A full tummy lasts about half a day. If he's left hungry or stinky for too long he gets sick 🤒. The **Diary** button shows everything that's happened to him.

The **Wardrobe** has a top hat, a beanie, a bow, shades, a scarf, and a crown that unlocks when he grows up. He can wear a hat, shades and a scarf all at once, and every accessory has a baby-sized version.

He lives on the ice outside his igloo, with mountains and a fishing hole. The sky follows your clock: dawn, day, dusk, and night with stars and an aurora (and a glowing igloo door). It's always night while he sleeps.

For now Sudo lives in your browser (`localStorage`), so everyone has their own Sudo. A shared version where everyone raises one Sudo together is the plan for later.

### Debug mode 🐞

Add `#debug` to the address ([valerie.wtf/#debug](https://valerie.wtf/#debug)) and a **Debug** button appears. It can switch stages, skip time, set any stat, trigger moods and animations, change the sky, unlock every accessory, turn snow off, and reset Sudo back to an egg. It changes your real saved Sudo.

## Package Panic 🎮

A typing game at [valerie.wtf/game](https://valerie.wtf/game). Package requests like "Arch: install git" fall from the top, and you type the right command (`sudo pacman -S git`) before they hit the floor. Combos multiply your score, it gets faster the longer you last, and every miss shows you the right answer. Pick `easy` (Mint, Ubuntu, Debian, Arch, Manjaro, Fedora and four tasks) or `hard` (every distro, every task).

## The old terminal

valerie.wtf used to be an interactive terminal for learning Linux package manager commands (APT, pacman, DNF, zypper and more). It still works at [valerie.wtf/archive/terminal-v2.html](https://valerie.wtf/archive/terminal-v2.html).

## How it's built

Each page is a single HTML file with plain HTML, CSS and JavaScript: no frameworks, no build step, no dependencies. It's hosted on GitHub Pages with the custom domain set in `CNAME`.

- `index.html`: Sudo
- `sprites/`: Sudo's 32×32 pixel-art sprites (`baby_*.png` for baby Sudo, `egg_*` and `hatch_*` for the egg, `acc_*` for accessories) and the 16×16 items. They're drawn by `tools/make_sprites.py` (needs Pillow: `python3 tools/make_sprites.py sprites preview.png`), so a new sprite is a few lines of Python
- `game/index.html`: Package Panic
- `archive/`: snapshots of older versions of the site, like `terminal-v1.html`, `terminal-v2.html` and `package-panic-v1.html`

To run it locally, open `index.html` in a browser.

## Contact

valeriecollins05(at)proton(dot)me

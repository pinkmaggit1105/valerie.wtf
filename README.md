# valerie.wtf

Tiny pixel pets live here. Pick one, hatch their egg, and look after them: feed them, bathe them, play with them, dress them up, clean up after them, and don't let them get sick.

**Live at [valerie.wtf](https://valerie.wtf)**

## The pets

| | Pet | Lives | Loves | Their thing |
| --- | --- | --- | --- | --- |
| 🐧 | **[Sudo](https://valerie.wtf/sudo/)** the penguin | on the ice next to his igloo | fish 🐟, his ball | Go **fishing** for fish, junk and a rare golden fish |
| 🪿 | **[Puck](https://valerie.wtf/puck/)** the goose | by the pond in the park | lettuce 🥬, her bell 🔔 | Help her **raid a picnic**: wait for them to look away, then snatch |

The home page shows a card for each pet with how they're doing right now, so you can see who needs you.

## Growing up

1. 🥚 **Egg.** Tap the egg to keep it warm. It cools off over time, and it only grows while it's warm (it shivers and turns blue when it's cold). After about 2½ warm hours it cracks open
2. 🐣 **Baby.** A fluffy chick (Sudo) or a yellow gosling (Puck) for the first 3 days
3. 🐧🪿 **Grown-up.** Sudo is a Tux-ish penguin with a little curl of a tuft. Puck is a white goose with a permanently suspicious eyebrow

## Looking after them

Drag an item from the tray onto your pet, or just tap it and it flies over:

| Sudo | Puck | What it does |
| --- | --- | --- |
| 🐟 Food | 🥬 Food | Feeds them from their pantry (tap it to pick what). Feed them when they're full and they get a tummy ache 🤢 |
| 🧼 Soap | 💦 Splash | Bath time. Scrub them with it and bubbles come off |
| 🎾 Ball | 🔔 Bell | Play. Makes them happy, but uses up energy and food |
| 💊 Meds | 💊 Meds | Only does anything when they're sick |
| 🎣 Fish! | 🧺 Snatch! | Their minigame |
| 🌙 Sleep | 🌙 Sleep | Puts them to bed, or wakes them up (they're grumpy about it) |

Tap your pet to pet them 🥰

Their food, fun, cleanliness and energy go down over time, even while the tab is closed, so come back and check on them. A full tummy lasts about half a day. Left hungry or dirty for too long, they get sick 🤒. A few minutes after eating, they poop 💩: tap it to clean it up, because poop lying around makes them dirty and a lot of it makes them ill.

**Pantry.** Food comes out of each pet's pantry: Sudo's fish bucket 🪣 and Puck's snack stash 🧺. Everyone starts with 5 of their basic food. Fish, strawberries and sandwiches you win in the minigames go into the pantry, and fancier treats come from the shop. Run out and the pantry points you to the minigame or the shop.

**Minigames.** Both work the same way: start, wait for the moment, then tap fast. Too early and it's ruined, too late and it's gone. Each game has a rare prize that unlocks an accessory (Sudo's golden fish unlocks a fish hat, Puck's stolen sun hat unlocks the sun hat), and the odds go up if you've been unlucky for a while.

**Coins and the shop 🪙** One coin purse is shared by every pet, and it shows on the home page and in each pet's header (tap it to open the shop). You earn coins by:

- **Looking after them when they need it:** feeding a hungry pet, bathing a dirty one, playing with a bored one, medicine when they're sick, scooping poop, warming a cold egg. Doing it when they don't need it earns nothing
- **Minigames:** every catch pays a few coins, and the rare prize pays 25. They pay out up to 60 coins a day
- **Visiting every day:** a daily bonus of 10 coins, plus 5 more for each day in a row (up to 40)
- **Milestones:** 20 when they hatch, 50 when they grow up

The shop sells treats (Sudo: fish, big fish, ice cream, fish tacos, a sushi platter; Puck: lettuce, strawberries, corn, sandwiches, cake) and six shop-only accessories for each pet: a chef's hat, monocle, pearls, pirate hat, wizard hat and halo.

**Wardrobe.** Sudo has 18 accessories and Puck has 16, each in a baby size and a grown-up size. They can wear one hat, one pair of shades and one neck thing at once. The crown unlocks when they grow up, the fish hat and sun hat come from the minigames, and six come from the shop.

**Their worlds** follow your clock: dawn, day, dusk, and night with stars and shooting stars. It's always night while they sleep. Sudo has an aurora, falling snow, a snowman and penguins waddling past. Puck has fireflies, falling leaves, a lamp post, a bench, the picnic she keeps robbing, and ducks paddling across the pond with their ducklings.

Every action has a little chiptune sound. The ♪ button turns them off. There are a few secrets too 👀

Each pet lives in your browser (`localStorage`), so everyone has their own.

### Debug mode 🐞

Add `#debug` to a pet's address ([valerie.wtf/sudo/#debug](https://valerie.wtf/sudo/#debug), [valerie.wtf/puck/#debug](https://valerie.wtf/puck/#debug)) and a **Debug** button appears. It can switch stages, skip time, set any stat, trigger moods and animations, make them poop, rig the minigame's rare prize, make the minigame instant, add 100 coins, fill the pantry, get the daily bonus again, send a shooting star or passers-by, change the sky, unlock every accessory, turn the weather off, and reset back to an egg. It changes your real saved pet.

## How it's built

Plain HTML, CSS and JavaScript: no frameworks, no build step, no dependencies. Hosted on GitHub Pages with the custom domain set in `CNAME`.

- `index.html`: the home page with a card for each pet
- `shared/core.js`: the rules every pet follows (stats, the egg, growing up, moods). No page code, so the home page can use it too
- `shared/pet.js` and `shared/pet.css`: the pet engine that builds each pet's page: care, dragging, the wardrobe, the minigame, the world, sounds and debug mode
- `sudo/` and `puck/`: each pet's page plus its `config.js`, which holds everything that makes that pet different: their text, items, accessories, minigame, and how to draw their world
- `sprites/sudo/`, `sprites/puck/`: 32×32 pixel-art sprites (`baby_*` for the baby, `egg_*` and `hatch_*` for the egg, `acc_*` for accessories) and 16×16 items
- `tools/`: the Python that draws every sprite (`pixels.py` has the shared bits, `sudo.py` and `puck.py` draw each pet). Run `python3 tools/make_sprites.py` (needs Pillow), or `python3 tools/make_sprites.py some/folder` to also get a preview sheet of each pet
- `archive/`: older versions of the site. valerie.wtf used to be a terminal for learning Linux package managers (`terminal-v1.html`, `terminal-v2.html`) with a typing game called Package Panic (`package-panic-v1.html`)

To add a pet: draw them in `tools/`, give them a folder with an `index.html` and a `config.js` (copy one of the existing pets), and add their config to the home page's script list.

To run it locally, serve the folder (for example `python3 -m http.server`) and open it in a browser.

## Contact

valeriecollins05(at)proton(dot)me

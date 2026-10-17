# valerie.wtf

An interactive terminal in your browser for learning Linux package manager commands. Pick a distro, type real commands, and the terminal explains what they do, or tells you off when you use the wrong package manager.

**Live at [valerie.wtf](https://valerie.wtf)**

## What it does

- **Pick a distro:** `use mint`, `use arch`, `use fedora`, ... and the prompt changes to match
- **Type real commands:** `sudo apt install firefox` shows simulated output and explains what it would do
- **Get corrected:** typing `pacman` on Mint, or forgetting `sudo`, shows the right command for your distro
- **Cheatsheets:** `cheatsheet` lists every basic command for your current distro
- **Compare:** `compare install` shows one task across every package manager side by side
- **Quiz:** `quiz` asks random "how do you X on distro Y?" questions and keeps score

Nothing actually runs. It's all simulated in the page, so feel free to type anything.

## Supported distros

| Package manager | Distros |
| --- | --- |
| APT | Linux Mint, Ubuntu, Debian, Pop!_OS |
| pacman | Arch Linux, Manjaro, EndeavourOS, CachyOS |
| DNF | Fedora, RHEL, Rocky Linux |
| zypper | openSUSE |
| apk | Alpine Linux |
| XBPS | Void Linux |
| Portage | Gentoo |
| Nix | NixOS |

It also covers **Flatpak** and **Snap**, which work on any distro (except Snap on Mint, which blocks it by default), and **yay** for the AUR on Arch-based distros.

## Commands

| Command | What it does |
| --- | --- |
| `help` | List everything |
| `distros` | Show all supported distros |
| `use <distro>` | Switch distro |
| `cheatsheet` | All commands for your current distro |
| `learn <task>` | One task in detail, with alternatives and tips |
| `compare <task>` | One task across every package manager |
| `about <manager>` | Everything about one package manager |
| `quiz` | Test yourself (`hint`, `skip`, `quit`) |
| `contact` | How to reach me |

Tasks: `refresh`, `upgrade`, `install`, `remove`, `search`, `info`, `list`, `orphans`, `clean`.

There are LOTS of easter eggs hidden in there too, like `neofetch`, `cowsay` and a `vim` you might never escape. And whatever you do, don't run `sudo rm -rf /` 👀

**Shortcuts:** ↑/↓ for command history, Tab to autocomplete, Ctrl+L to clear. On phones, use the buttons at the bottom.

## How it's built

It's a single `index.html` with plain HTML, CSS and JavaScript: no frameworks, no build step, no dependencies. It's hosted on GitHub Pages with the custom domain set in `CNAME`.

To run it locally, just open `index.html` in a browser.

### Adding a distro or command

All the data lives at the top of the `<script>` in `index.html`:

- `DISTROS` maps a distro to its package manager
- `MANAGERS` has each package manager's commands per task. The first command in each list is the one the terminal teaches, and the others are accepted alternatives. `PKG` is the placeholder for a package name
- `EXTRAS` holds the managers that aren't tied to one distro (Flatpak, Snap, yay)

## Contact

valeriecollins05(at)proton(dot)me

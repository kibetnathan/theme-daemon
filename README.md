# theme-daemon

Theme daemon for the `~/.config/` ecosystem. Detects macOS dark/light mode switches and applies Catppuccin Mocha / Latte themes across all configured tools.

## Quick start

```bash
theme-daemon.sh start    # Launch background daemon (polls every 2s)
theme-daemon.sh stop     # Kill daemon
theme-daemon.sh restart  # Restart daemon
theme-daemon.sh status   # Check if running
theme-daemon.sh once     # Apply current theme once, then exit
theme-daemon.sh logs     # View logs (tail|last for variants)
```

## How it works

On a configurable poll interval (every 2s) the daemon checks `defaults read -g AppleInterfaceStyle`. When the system toggles dark/light, it loads the corresponding Catppuccin palette (`colors/palette-mocha.json` or `colors/palette-latte.json`) and calls every registered plugin. Each plugin writes its theme change, and if it reports that files were modified, the engine calls its optional `reload()` step.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  theme-daemon.py            theme-daemon.sh             │
│  (orchestrator + CLI)       (start/stop/status wrapper) │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│                    ThemeEngine                          │
│  core.py — poll loop, palette loading, plugin dispatch  │
│  port.py  — ToolPlugin ABC                              │
└───────────────┬─────────────────────────────────────────┘
                │
    ┌───────────┼───────────────┬──────────────────┐
    ▼           ▼               ▼                  ▼
┌────────┐ ┌────────┐  ┌──────────────┐   ┌──────────────┐
│ bat    │ │ tmux   │  │ sketchybar   │   │  wallpaper   │
│ simple │ │ 2-way  │  │ palette_     │   │  bash script │
│ line   │ │ swap + │  │ rewrite      │   │  per-space   │
│ replace│ │ reload │  │ + reload     │   │  osascript   │
└────────┘ └────────┘  └──────────────┘   └──────────────┘
```

## Plugins

| Plugin     | Config file                        | Approach                                                                              |
| ---------- | ---------------------------------- | ------------------------------------------------------------------------------------- |
| bat        | `~/.config/bat/config`             | `line_replace` — swaps `--theme` string                                               |
| ghostty    | `~/.config/ghostty/config`         | `line_replace` — theme + opacity (returns `a or b`)                                   |
| btop       | `~/.config/btop/btop.conf`         | `line_replace` — swaps `color_theme` value                                            |
| tmux       | `~/.config/tmux/tmux.conf`         | `line_replace` — swaps `@catppuccin_flavor`                                           |
| borders    | `~/.config/borders/bordersrc`      | Custom rewrite — ARGB computation from palette, kills + restarts process              |
| sketchybar | `~/.config/sketchybar/colors.sh`   | `palette_rewrite` — bulk replace all `export VAR=0x...` lines                         |
| fastfetch  | `~/.config/fastfetch/config.jsonc` | Custom rewrite — hardcoded 256-color ANSI mapping, bidirectional swap                 |
| newtab     | (hardcoded HTML)                   | `line_replace` — swaps hex color in page template                                     |
| opencode   | `~/.config/opencode/tui.json`      | `line_replace` — swaps `catppuccin-mocha`/`catppuccin-latte`                          |
| yabai      | `~/.config/yabai/yabairc`          | `line_replace` — swaps `insert_feedback_color`, restarts service                      |
| wallpaper  | `wallpapers/wallpaper.json`        | Custom package (`plugins/wallpaper/`) — reads config, delegates to `set-wallpaper.sh` |

## Project layout

```
~/.config/.manager/
├── engine/
│   ├── port.py          # ToolPlugin ABC
│   └── core.py          # ThemeEngine — poll, palette, dispatch
├── plugins/
│   ├── __init__.py      # Plugin registration
│   ├── _base.py         # Shared helpers (line_replace, palette_rewrite, shell)
│   ├── bat.py           # One file per plugin
│   ├── borders.py
│   ├── btop.py
│   ├── fastfetch.py
│   ├── ghostty.py
│   ├── newtab.py
│   ├── opencode.py
│   ├── sketchybar.py
│   ├── tmux.py
│   ├── yabai.py
│   └── wallpaper/              # Package-based plugin
│       ├── __init__.py
│       └── set-wallpaper.sh
├── colors/
│   ├── palette-mocha.json      # Catppuccin dark palette
│   └── palette-latte.json      # Catppuccin light palette
├── wallpapers/
│   ├── wallpaper.json          # Dark/light wallpaper path mapping
│   └── images/                 # Wallpaper image files
├── cache/                      # Runtime logs (gitignored)
├── theme-daemon.py             # Python entry point
├── theme-daemon.sh             # Shell wrapper
├── README.md
└── PLUGINS.md                  # Plugin development guide
```

## Adding a plugin

1. Create a file in `plugins/` (or a directory with `__init__.py` for bundled scripts)
2. Subclass `ToolPlugin`, implement `name` and `apply()`, optionally `reload()`
3. Add it to `plugins/__init__.py:all_plugins()`

See [PLUGINS.md](PLUGINS.md) for the full guide.

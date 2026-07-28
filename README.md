# .manager

System configuration management for `~/.config/`. Documents how every tool handles styling and automatically swaps Catppuccin themes when macOS switches between dark and light mode.

## Architecture

Hexagonal (ports & adapters) — the core logic processes theme changes, while tool-specific adapters are isolated as plugins.

```
                   ┌─────────────┐
                   │ ThemeEngine │  ← core hexagon
                   │  (core.py)  │
                   └──────┬──────┘
                          │ ToolPlugin  ← port (port.py)
                          │ (ABC)
              ┌───────────┼───────────┐
              │           │           │
         ┌────┴───┐  ┌───┴────┐  ┌──┴────┐
         │ bat    │  │ghostty │  │ tmux  │  ← adapters (plugins/)
         ├────────┤  ├────────┤  ├───────┤
         │btop    │  │borders │  │yabai  │
         ├────────┤  ├────────┤  ├───────┤
         │fastfetch│  │newtab │  │sketchybar
         └────────┘  └────────┘  └───────┘
```

## Files

| File / Directory | Purpose |
|------------------|---------|
| `engine/port.py` | `ToolPlugin` ABC — the port interface all plugins implement |
| `engine/core.py` | `ThemeEngine` — orchestrates palette loading, theme detection, and plugin execution |
| `plugins/` | Adapter directory — one file per tool, each implementing `ToolPlugin` |
| `plugins/_base.py` | Shared helpers (`line_replace`, `palette_rewrite`, `shell`) |
| `theme-daemon.py` | Entry point — wires engine and plugins together, handles CLI args |
| `theme-daemon.sh` | Shell wrapper for start/stop/status/restart/once |
| `styling-config.md` | Reference documenting how all tools in `~/.config/` manage appearance |
| `styling-classification.json` | Categorized index of tools (GUI apps, CLI/TUI, no styling) |
| `colors/palette-mocha.json` | Catppuccin Mocha hex color values |
| `colors/palette-latte.json` | Catppuccin Latte hex color values |
## Theme Daemon

Auto-switches configured tools between Catppuccin Mocha (dark mode) and Catppuccin Latte (light mode).

### Usage

```
theme-daemon-start    Launch background daemon (polls every 2s)
theme-daemon-stop     Kill daemon
theme-daemon-status   Check if running
theme-daemon-restart  Restart daemon
theme-daemon-once     Apply current theme once, then exit
```

Aliases are defined in `.zshrc`.

### Active plugins

| Plugin | What it does |
|--------|-------------|
| **bat** | Swaps `--theme` between Mocha and Latte |
| **ghostty** | Swaps theme + background opacity |
| **btop** | Swaps `color_theme` between mocha and latte |
| **tmux** | Swaps `@ukiyo-theme`, runs `tmux source-file` |
| **borders** | Rewrites active/inactive/bg colors in ARGB, restarts daemon |
| **sketchybar** | Rewrites all color variables in `colors.sh`, runs `sketchybar --reload` |
| **fastfetch** | Swaps ANSI 256-color codes in `config.jsonc` |
| **newtab** | Swaps page background color in `newtab.html` |
| **yabai** | Swaps `insert_feedback_color`, runs `yabai --restart-service` |

### Adding a new plugin

Create a class in `plugins/` that extends `ToolPlugin` (from `engine.port`), implement `name` and `apply()`, then register it in `plugins/__init__.py`.

### Logs

Daemon output goes to `/tmp/theme-daemon.log`.

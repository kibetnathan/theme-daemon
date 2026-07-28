# .manager — agent instructions

## Architecture

- **Hexagonal (ports & adapters):** `engine/port.py` defines `ToolPlugin` ABC; `engine/core.py` is `ThemeEngine`; `plugins/*.py` (or `plugins/*/__init__.py` for bundled plugins) are adapters.
- **Registration:** Add new plugins to `plugins/__init__.py` `all_plugins()` — no auto-discovery.
- **Entry point** `theme-daemon.py` — wires engine + plugins. Shell wrapper `theme-daemon.sh` for start/stop/status/restart/once/logs.
- **macOS only** — uses `defaults read -g AppleInterfaceStyle`, `osascript`, macOS-specific tools (yabai, sketchybar, borders).

## Commands

```bash
theme-daemon.sh start|stop|status|restart|once|logs [tail|last]
theme-daemon.py once|logs|pid        # direct python entry
```

- Daemon polls every 2s for dark/light switch.
- Runs via `nohup`, PID at `/tmp/theme-daemon.pid`.
- Logs: `cache/theme-daemon/logs/theme-daemon-YYYY-MM-DD.log` (rotated at 10 MB, retained 7 days). Cache dir is gitignored.
- Uses `loguru` — import from `loguru import logger`.

## Plugin contract

1. Subclass `ToolPlugin` from `engine.port`, implement `name` (property) and `apply(self, palette: dict, is_dark: bool) -> bool`.
2. `apply()` must return `True` if it changed files — only then is `reload()` called (see `engine/core.py:44`).
3. Optional `reload()` for post-apply commands (fire-and-forget via `_base.shell()`).

## Shared helpers (`plugins/_base.py`)

- `line_replace(path, [(search, dark_val, light_val)], is_dark)` — at most **1** replacement per search string.
- `palette_rewrite(path, palette)` — rewrites all `export VAR=0x[0-9a-fA-F]{8}` lines using palette dict keys (lowercased).
- `shell(cmd)` — `Popen` fire-and-forget.
- `restart_borders_process()` — kills `borders` then re-sources `bordersrc`.

## Plugin quirks

| Plugin | Approach | Notes |
|--------|----------|-------|
| bat | `line_replace` | Theme string in bat config |
| ghostty | `line_replace` (×2) | Returns `a or b` — changes theme + opacity |
| btop | `line_replace` | Straight theme swap |
| tmux | custom regex | Swaps `@ukiyo-theme` value, reloads via `tmux source-file` |
| borders | custom file rewrite | Inline ARGB computation (`0x{alpha}{rgb}`), always kills + restarts |
| sketchybar | `palette_rewrite` | Reloads via `sketchybar --reload` |
| fastfetch | custom ANSI map | Hardcoded 256-color mapping (not palette-based), bidirectional swap |
| newtab | `line_replace` | Hardcoded hex colors, not palette-based |
| opencode | `line_replace` (×2) | Bidirectional swap between `catppuccin-mocha` / `catppuccin-latte` in `tui.json` |
| wallpaper | custom (`plugins/wallpaper/` package) | Reads `wallpaper.json`, delegates to `set-wallpaper.sh` (yabai + osascript per space). |
| yabai | `line_replace` | Trailing `\\` matters, restarts yabai service |

## Palette files

- `palette-mocha.json` (dark) and `palette-latte.json` (light) — Catppuccin hex colors (no `#` prefix).
- `wallpaper.json` — maps `"dark"` and `"light"` keys to wallpaper image paths (uses `~` expansion).
- Keys: base, mantle, crust, text, subtext0/1, surface0/1/2, overlay0/1/2, blue, lavender, sapphire, sky, teal, green, yellow, peach, maroon, red, mauve, pink, flamingo, rosewater.

## Testing / tooling

- **Linter:** `ruff` — run `ruff check .` before committing.
- **CI:** GitHub Actions runs `astral-sh/ruff-action@v3` on push/PR to `main` (`.github/workflows/lint.yml`).
- **Manual testing:** `theme-daemon once`.

## Git style

- Conventional commits (`feat`, `chore`, etc.). Single `main` branch.

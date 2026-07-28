# Writing plugins

## The contract

Every plugin is a class that inherits from `ToolPlugin` (defined in `engine/port.py`):

```python
from abc import ABC, abstractmethod

class ToolPlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def apply(self, palette: dict, is_dark: bool) -> bool:
        ...

    def reload(self) -> None:
        pass
```

| Method | Required | Purpose |
|--------|----------|---------|
| `name` | Yes | Unique plugin identifier (used in logs) |
| `apply(palette, is_dark)` | Yes | Apply the theme. Return `True` if files were changed — only then `reload()` is called |
| `reload()` | No | Fire-and-forget post-apply command (restart a service, re-source config, etc.) |

### `palette` contents

A dict with Catppuccin hex color values (no `#` prefix):

```
base, mantle, crust, text, subtext0, subtext1,
surface0, surface1, surface2, overlay0, overlay1, overlay2,
blue, lavender, sapphire, sky, teal, green, yellow,
peach, maroon, red, mauve, pink, flamingo, rosewater
```

### Two flavours per palette

| Parameter | Mocha (dark) | Latte (light) |
|-----------|-------------|---------------|
| `is_dark` | `True` | `False` |
| `palette` | `colors/palette-mocha.json` | `colors/palette-latte.json` |

## Registration

1. Import your class in `plugins/__init__.py`
2. Add an instance to the `all_plugins()` list

```python
from .myplugin import MyPlugin

def all_plugins():
    return [
        ...
        MyPlugin(),
    ]
```

Plugins run in list order — wallpaper is last so yabai (which wallpaper depends on) runs first.

## Shared helpers (`plugins/_base.py`)

### `line_replace(path, replacements, is_dark)`

The simplest and most common approach. At most **1 replacement per search string**.

```python
line_replace("~/.config/bat/config", [
    ('--theme="Catppuccin Mocha"', '--theme="Catppuccin Mocha"', '--theme="Catppuccin Latte"'),
    ('--theme="Catppuccin Latte"', '--theme="Catppuccin Mocha"', '--theme="Catppuccin Latte"'),
], is_dark)
```

Each tuple is `(search, dark_value, light_value)`:
- `search` — literal string to find in the file (must be unique enough to match once)
- `dark_value` — what to replace it with when `is_dark=True`
- `light_value` — what to replace it with when `is_dark=False`

The pattern of including both old and new values in the replacement list makes it idempotent: if the file is already in the target state, nothing changes.

### `palette_rewrite(path, palette)`

Rewrites every line matching `export VAR=0x[0-9a-fA-F]{8}` using the lowercased variable name as a palette key. Designed for sketchybar's `colors.sh`:

```python
palette_rewrite("~/.config/sketchybar/colors.sh", palette)
```

If `colors.sh` contains:

```bash
export MAUVE=0xffcba6f7
export LAVENDER=0xffb4befe
```

It becomes the Latte equivalent when the palette is loaded.

### `shell(cmd)`

Fire-and-forget subprocess. Used in `reload()`:

```python
def reload(self):
    shell("sketchybar --reload")
```

### `restart_borders_process()`

Kills `borders` then re-sources `~/.config/borders/bordersrc`. Implements the restart logic for the borders plugin specifically, since borders has no reload signal.

## Writing styles

### 1. Straight theme swap with `line_replace` (bat, btop)

```python
from engine.port import ToolPlugin
from ._base import line_replace

class BatPlugin(ToolPlugin):
    @property
    def name(self):
        return "bat"

    def apply(self, palette, is_dark):
        target = '--theme="Catppuccin Mocha"' if is_dark else '--theme="Catppuccin Latte"'
        return line_replace("~/.config/bat/config", [
            ('--theme="Catppuccin Mocha"', target, target),
            ('--theme="Catppuccin Latte"', target, target),
        ], is_dark)
```

### 2. Multiple `line_replace` calls, OR the result (ghostty)

Swaps two independent lines (theme and opacity). Returns `a or b` so `apply()` reports `True` if either changed:

```python
def apply(self, palette, is_dark):
    a = line_replace(c, [
        ("theme = Catppuccin Mocha", "theme = Catppuccin Mocha", "theme = Catppuccin Latte"),
    ], is_dark)
    b = line_replace(c, [
        ("background-opacity = 0.66" if is_dark else "background-opacity = 0.85",
         "background-opacity = 0.66",
         "background-opacity = 0.85"),
    ], is_dark)
    return a or b
```

### 3. Custom file rewrite with palette colors (borders)

Compute ARGB values from palette keys and regex-replace them inline:

```python
def apply(self, palette, is_dark):
    path = os.path.expanduser("~/.config/borders/bordersrc")
    with open(path) as f:
        content = f.read()

    for color_key, alpha in [("mauve", "ff"), ("lavender", "dd"), ("mantle", "60")]:
        argb = f"0x{alpha}{palette[color_key]}"
        name = {"mauve": "active", "lavender": "inactive", "mantle": "background"}[color_key]
        content = re.sub(rf"{name}_color=0x[0-9a-fA-F]{{8}}", f"{name}_color={argb}", content)

    with open(path, "w") as f:
        f.write(content)
    restart_borders_process()
    return True
```

### 4. Palette bulk rewrite + reload (sketchybar)

Uses `palette_rewrite` for bulk color variable replacement and adds a `reload` step:

```python
from ._base import palette_rewrite, shell

class SketchybarPlugin(ToolPlugin):
    @property
    def name(self):
        return "sketchybar"

    def apply(self, palette, is_dark):
        return palette_rewrite("~/.config/sketchybar/colors.sh", palette)

    def reload(self):
        shell("sketchybar --reload")
```

`palette_rewrite` matches `export VAR=0x[0-9a-fA-F]{8}` lines and replaces the hex value using `palette[var.lower()]`. The file must follow that exact format.

### 5. Delegating to a bash script (wallpaper)

For complex workflows that don't fit in a `line_replace`, create a package (`plugins/wallpaper/`) and call a shell script from `apply()`:

```python
import json, os, subprocess
from loguru import logger
from engine.port import ToolPlugin

class WallpaperPlugin(ToolPlugin):
    @property
    def name(self):
        return "wallpaper"

    def apply(self, palette, is_dark):
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "wallpapers", "wallpaper.json")
        with open(config_path) as f:
            config = json.load(f)
        path = os.path.expanduser(config["dark" if is_dark else "light"])
        script = os.path.join(os.path.dirname(__file__), "set-wallpaper.sh")
        r = subprocess.run(["bash", script, path], capture_output=True, text=True, check=False)
        return r.returncode == 0
```

The bash script lives beside the `__init__.py` inside the plugin package and receives the target path as an argument:

```bash
#!/bin/bash
WALLPAPER_PATH="$1"
osascript -e "tell application \"System Events\" to set picture of every desktop to POSIX file \"$WALLPAPER_PATH\""
```

This keeps complex shell logic testable and decoupled.

## Tips

- **Return `True` only if files changed.** The engine checks the return value before calling `reload()` — skipping unnecessary restarts is both faster and avoids visual flicker.
- **Use `line_replace` when possible.** It's concise, idempotent, and handles edge cases (missing files, already-applied state).
- **Make plugins idempotent.** Running `theme-daemon.sh once` twice should produce the same result as running it once.
- **Log your work.** Use `logger.info()`, `logger.warning()`, `logger.error()` from `loguru`. They'll appear in the rotating log files in `cache/theme-daemon/logs/`.
- **Bundled scripts.** If your plugin needs more than ~20 lines of shell, put it in a subdirectory with `__init__.py + script.sh` rather than inlining everything in Python.
- **macOS-only.** The daemon uses `defaults read -g AppleInterfaceStyle`, `osascript`, and macOS window manager tools (yabai, sketchybar, borders). Plugins targeting other platforms must handle detection themselves.

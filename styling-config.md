# Styling Configuration Reference

How every tool in `~/.config/` manages its appearance (themes, colors, fonts, UI).

See [`styling-classification.json`](styling-classification.json) for a categorized index
(grouped as GUI apps, CLI/TUI tools, and tools with no styling capability).

---

## bat

| File | Purpose |
|------|---------|
| `bat/config` | Theme selection via `--theme` flag |

**How it works:** Single `--theme` flag selects a built-in `.tmTheme` (Sublime Text syntax scheme). Currently set to `"Catppuccin Mocha"`. No custom theme files installed. The theme handles all syntax-highlighting colors for every token type (keywords, strings, comments, etc.).

---

## borders

| File | Purpose |
|------|---------|
| `borders/bordersrc` | Shell script launching the `borders` daemon with visual params |

**How it works:** Inline key=value options in a Bash script passed to the `borders` binary. Styling params include `style=round`, `width=6.0`, `hidpi=on`, and three colors in `0xAABBGGRR` (BGRA hex with alpha):
- `active_color=0xc0cba6f7` — mauve at 75% opacity
- `inactive_color=0xc0b4befe` — peach at 75% opacity
- `background_color=0x30181825` — near-black at 19% opacity

---

## btop

| File | Purpose |
|------|---------|
| `btop/btop.conf` | Main config; theme, graph symbols, visual layout |
| `btop/themes/catppuccin-mocha.theme` | Custom theme file (broken/404 on this system) |

**How it works:** `color_theme = "catppuccin-mocha"` selects a `.theme` file from `~/.config/btop/themes/` or the system share dir. `theme_background = true` controls whether the theme's background color is used. `truecolor = true` enables 24-bit color. `graph_symbol = "braille"` selects graph rendering style. `rounded_corners = true` controls box corner style. `clock_format = "%X"` enables a clock in the header.

---

## cagent

**No styling configuration.** Directory only contains a first-run marker and a user UUID file. cagent appears to be a headless CLI agent with no customizable appearance.

---

## darktable

| File | Purpose |
|------|---------|
| `darktable/darktablerc-common` | Theme and font settings (shared across versions) |
| `darktable/darktablerc` | Main config; UI layout, color management, per-module settings |

**How it works:** Theme is set via `ui_last/theme=darktable-elegant-grey` in `darktablerc-common`. `font_size=12.0` controls UI font size. `use_system_font=false` uses darktable's bundled font. `themes/usercss=false` disables custom CSS theming. The main `darktablerc` stores color management profiles, overexposure indicator colors, overlay colors, and per-module visualization settings (graph heights, channel selections, etc.).

---

## fastfetch

| File | Purpose |
|------|---------|
| `fastfetch/config.jsonc` | Primary config; colors, separators, layout, modules |
| `fastfetch/config_backup.jsonc` | Backup/default-style config |
| `fastfetch/logos/kaneki.png` | Custom ASCII/image logo |

**How it works:** JSONC config defines `logo.padding` and `logo.color` for the logo's ANSI color codes. `display.separator` is a custom ANSI-colored arrow `->`. Modules are individually styled with `outputColor`, `keyColor`, and custom `format` strings using inline ANSI escape sequences and Nerd Font icons. The color palette follows Catppuccin Mocha using 256-color ANSI codes. Custom modules draw decorative borders (`┌`,`┐`,`└`,`┘`) and color spectrum rows with Nerd Font `` chars.

---

## ghostty

| File | Purpose |
|------|---------|
| `ghostty/config` | Primary terminal config |
| `ghostty/config.ghostty` | Alternative/secondary config |
| `ghostty/shaders/boo-cursor.glsl` | Active GPU cursor shader (smear trail) |
| `ghostty/shaders/wisp-cursor.glsl` | Alternative shader (brush-stroke style) |
| `ghostty/shaders/tinkle-cursor.glsl` | Alternative shader (elastic bounce) |

**How it works:** Styling is split across three layers:
1. **Config keys** — `theme = Catppuccin Mocha` (built-in theme for ANSI/fg/bg/cursor colors), `background-opacity = 0.66`, `window-colorspace = display-p3`, `window-decoration = false`, `font-family = "MesloLGS NF"`, `font-size = 16`, `cursor-style = block`
2. **custom-shader** — `shaders/boo-cursor.glsl` loaded as a GLSL fragment shader running per-frame on the GPU, producing a directional smear-trail animation
3. **Shader constants** — color (`TRAIL_COLOR` reads `iCurrentCursorColor` from the theme), alpha, animation length, blur, trail size

---

## git

| File | Purpose |
|------|---------|
| `git/ignore` | Global gitignore (1 line, no styling) |
| `git/gitk` | gitk GUI config (colors, fonts, geometry) |

**How it works:** `gitk` stores extensive styling: `bgcolor`, `fgcolor`, `colors` (array of 8 colors for graph lines), `diffcolors`, `diffbgcolors`, `mainfont`, `textfont`, `uifont`, `tabstop`, `selectbgcolor`, `foundbgcolor`, `headbgcolor`, `tagbgcolor`, and ~30+ other color/geometry settings. The `theme aqua` selection applies macOS-native appearance. Global `git/ignore` and regular git config (`~/.gitconfig`) handle color.ui and pager settings outside this directory.

---

## herd-lite

**No styling configuration.** Directory contains only a PHP binary, Composer, Laravel installer, CA bundle, and a minimal `php.ini` with no styling/color settings.

---

## htop

| File | Purpose |
|------|---------|
| `htop/htoprc` | All settings; colors, layout, meters |

**How it works:** `color_scheme=0` selects one of htop's built-in color schemes (0=default, 1=monochrome, 2=black on white, etc.). `highlight_megabytes=1`, `highlight_threads=1`, `highlight_deleted_exe=1` control visual emphasis. `header_layout=two_50_50` + `column_meters_0/1` define which meters appear (LeftCPUs, Memory, Swap, RightCPUs, Tasks, LoadAverage, Uptime) and their display modes (`1`=bar, `2`=text). The file is auto-rewritten by htop when settings change in the UI.

---

## jgit

**No styling configuration.** Single auto-generated `config` file with filesystem timestamp-resolution tuning only.

---

## mpm

**No styling configuration.** Single `config.yml` with only an `exclude` list of package managers to ignore.

---

## newtab

| File | Purpose |
|------|---------|
| `newtab/newtab.html` | Self-contained HTML page with inline CSS |

**How it works:** All styling is inline CSS in a single HTML file. Hardcoded dark theme (`background: #0d0d0d`, `color: white`). Font stack `"SF Pro Display", -apple-system, sans-serif`. Card component with frosted-glass effect (`rgba(255,255,255,0.06)` bg, `16px` border-radius). Time at `72px`/weight `200`, date at `16px`/uppercase. No theme switching, no external files, no JS styling logic — just static CSS in a `<style>` block.

---

## nvim

| File | Purpose |
|------|---------|
| `nvim/lua/plugins/colorscheme.lua` | Theme registration and active theme selection |
| `nvim/lua/config/lazy.lua` | Lazy.nvim bootstrap; fallback colorscheme for install |
| `nvim/lua/plugins/snacks.lua` | Dashboard with ASCII art header |
| `nvim/lua/config/options.lua` | Additional Neovim visual options (empty, uses LazyVim defaults) |

**How it works:** LazyVim-based config. Five theme plugins registered: Kanagawa, Catppuccin (active, flavour=mocha, treesitter integration), Rose Pine, Tokyo Night, Gruvbox. Active theme set via `colorscheme = "catppuccin"` in LazyVim opts. Fallback for first install: `{ "tokyonight", "habamax" }`. Snacks dashboard renders a large ASCII art dragon with "CATPPUCCIN" text. All visual aspects (statusline, bufferline, which-key, telescope, completion) inherit from the active colorscheme via LazyVim defaults.

---

## nvim-backup

Same structure and styling configuration as `nvim` (identical colorscheme.lua, lazy.lua, snacks.lua). Backup of the active config.

---

## nvim-kickstart

| File | Purpose |
|------|---------|
| `nvim-kickstart/init.lua` | Self-contained 1008-line config with all styling inline |
| `nvim-kickstart/.stylua.toml` | Lua code formatter style (160col, 2-space, single quotes) |

**How it works:** Single-file config. Two themes installed: Catppuccin (active, `vim.cmd.colorscheme 'catppuccin'` with defaults) and Tokyo Night (configured but not activated, comments italic disabled). `vim.g.have_nerd_font = true` enables Nerd Font icons across which-key, mini.statusline, mini.icons, blink.cmp, neo-tree. mini.statusline for statusline (icons on, custom LINE:COL format). which-key with zero delay and grouped leader mappings. Telescope's ui-select uses dropdown theme. Diagnostics use rounded borders, virtual_lines instead of virtual_text. Git signs in gutter with custom Unicode chars. Visual options: `number`, `relativenumber`, `cursorline`, `signcolumn=yes`, custom `listchars`, `inccommand=split`, `scrolloff=10`.

---

## opencode

| File | Purpose |
|------|---------|
| `opencode/opencode.jsonc` | Config (3 lines, empty schema reference only) |

**How it works:** No active styling configuration. The config file only contains a `$schema` reference. Styling (themes, colors) would be configured within this file via the opencode JSONC schema, but none are currently set.

---

## psysh

**No styling configuration.** Directory only contains a manual update check JSON file and a shell history file. PsySH uses terminal ANSI colors by default with no custom theme configuration in this directory.

---

## raycast

**No styling configuration in `~/.config/raycast/`.** This directory contains only extension bundles (compiled JS) and an empty `ai/` directory. Raycast themes are stored in `~/Library/Application Support/com.raycast.macos/` (outside the scope of `~/.config/`). The `extensions/` directory contains compiled extension code (e.g., Translate extension) with no theme/color config.

---

## sketchybar

| File | Purpose |
|------|---------|
| `sketchybar/sketchybarrc` | Main config; bar appearance, defaults, item sources |
| `sketchybar/colors.sh` | Catppuccin Mocha color palette (35+ exported variables) |
| `sketchybar/icons.sh` | Nerd Font icon mappings for all bar items |
| `sketchybar/userconfig.sh` | Dynamic Island sizing, colors, font config |
| `sketchybar/helper/helper.c` | C helper for CPU/memory data (compiled to `helper`) |

**How it works:** Layered sourcing: `sketchybarrc` sources `colors.sh`, `icons.sh`, and `userconfig.sh` at startup. Bar config: `blur_radius=30`, `color=$BASE`, `corner_radius=9`, `height=37`, `margin=10`. Default icon/label/background/popup styles defined as arrays with font, color, padding, and corner-radius. `colors.sh` exports the full Catppuccin Mocha palette (~35 colors) in `0xAARRGGBB` hex. `icons.sh` exports ~50 Nerd Font glyph variables. `userconfig.sh` defines Dynamic Island dimensions, corner radii, animation squish, per-island sizing (music, volume, brightness, wifi, battery, notification, app-switch), and per-island colors.

---

## skhd

**No styling configuration.** `skhdrc` contains only keybinding definitions. skhd is a background hotkey daemon with no visual output.

---

## t

**No styling configuration.** `/Users/nero/.config/t` is an empty 0-byte file, not a directory. The `t` tool is not installed on this system.

---

## tmux

| File | Purpose |
|------|---------|
| `tmux/tmux.conf` | All tmux config; theme, colors, plugins |
| `tmux/plugins/tmux-ukiyo/` | Ukiyo theme plugin (Catppuccin-based) |

**How it works:** `set-option -sa terminal-overrides ",xterm*:Tc"` enables true color. Ukiyo theme loaded via TPM: `set -g @ukiyo-theme "catppuccin/mocha"`. `window-style 'bg=default'` and `window-active-style 'bg=default'` enable transparent pane backgrounds. `terminal-overrides ",xterm-256color:Tc"` ensures true-color passthrough. The Ukiyo plugin handles the status bar colors, pane borders, and other UI chrome.

---

## yabai

| File | Purpose |
|------|---------|
| `yabai/yabairc` | Window manager config; gaps, padding, shadows, borders |

**How it works:** Single shell script setting yabai config keys. Styling-relevant settings:
- `window_shadow float` — drop shadows on floating windows
- `insert_feedback_color 0xffa6e3a1` — green insertion indicator color
- `top_padding 8`, `bottom_padding 8`, `left_padding 8`, `right_padding 8` — workspace margins
- `window_gap 10` — gap between windows
- Also launches `borders` as a subprocess with matching Catppuccin colors

---

## zed

| File | Purpose |
|------|---------|
| `zed/settings.json` | All settings; themes, fonts, icon theme |
| `zed/themes/` | Custom theme directory (empty) |

**How it works:** Theme selection via nested config:
- `theme.mode = "system"` — auto-switches with macOS appearance
- `theme.dark = "Catppuccin Mocha"`, `theme.light = "Catppuccin Latte"`
- `icon_theme.mode = "system"` with Zed (Default) for both modes
- `ui_font_size = 16`, `buffer_font_size = 15`
- No `buffer_font_family` or `ui_font_family` set (uses system defaults: SF Mono / San Francisco)
- The `themes/` directory is empty; themes come from Zed's built-in set or extensions

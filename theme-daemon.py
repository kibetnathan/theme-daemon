#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import time
import signal
import logging

MANAGER = os.path.expanduser("~/.config/.manager")
PID_FILE = "/tmp/theme-daemon.pid"
LOG_FILE = "/tmp/theme-daemon.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)

palettes = {}
mapping = None


def load():
    global palettes, mapping
    palettes["mocha"] = json.load(open(f"{MANAGER}/palette-mocha.json"))
    palettes["latte"] = json.load(open(f"{MANAGER}/palette-latte.json"))
    mapping = json.load(open(f"{MANAGER}/theme-mapping.json"))


def rgb_to_argb(rgb_hex, alpha="c0"):
    return f"0x{alpha}{rgb_hex}"


def rgb_to_sketchybar(rgb_hex):
    return f"0xff{rgb_hex}"


def is_dark():
    r = subprocess.run(
        ["defaults", "read", "-g", "AppleInterfaceStyle"],
        capture_output=True,
        text=True,
    )
    return r.stdout.strip() == "Dark"


def apply_to_file(path, replacements, is_dark_mode):
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        logging.warning(f"File not found: {path}")
        return False
    with open(path) as f:
        content = f.read()
    changed = False
    for r in replacements:
        search = r["search"]
        target = r["dark"] if is_dark_mode else r["light"]
        if search in content:
            if content.replace(search, target, 1) != content:
                content = content.replace(search, target, 1)
                changed = True
    if changed:
        with open(path, "w") as f:
            f.write(content)
        logging.info(f"Updated {path}")
    return changed


def apply_sketchybar(is_dark_mode):
    path = os.path.expanduser("~/.config/sketchybar/colors.sh")
    if not os.path.isfile(path):
        logging.warning("sketchybar colors.sh not found")
        return
    palette = palettes["mocha"] if is_dark_mode else palettes["latte"]
    with open(path) as f:
        content = f.read()
    changed = False

    def replace_color(m):
        var = m.group(1)
        key = var.lower()
        if key in palettes["mocha"] or key in palettes["latte"]:
            new_val = rgb_to_sketchybar(palette[key])
            return f"export {var}={new_val}"
        return m.group(0)

    new_content = re.sub(
        r"^export (\w+)=0x[0-9a-fA-F]{8}", replace_color, content, flags=re.MULTILINE
    )
    if new_content != content:
        with open(path, "w") as f:
            f.write(new_content)
        logging.info("Updated sketchybar/colors.sh")
        changed = True
    return changed


def apply_borders(is_dark_mode):
    path = os.path.expanduser("~/.config/borders/bordersrc")
    if not os.path.isfile(path):
        return False
    palette = palettes["mocha"] if is_dark_mode else palettes["latte"]
    with open(path) as f:
        content = f.read()
    changed = False
    active_rgb = palette["mauve"]
    inactive_rgb = palette["lavender"]
    bg_rgb = palette["mantle"]
    active_bgra = rgb_to_argb(active_rgb)
    inactive_bgra = rgb_to_argb(inactive_rgb)
    bg_bgra = rgb_to_argb(bg_rgb, alpha="30")
    content = re.sub(
        r"active_color=0x[0-9a-fA-F]{8}", f"active_color={active_bgra}", content
    )
    content = re.sub(
        r"inactive_color=0x[0-9a-fA-F]{8}", f"inactive_color={inactive_bgra}", content
    )
    content = re.sub(
        r"background_color=0x[0-9a-fA-F]{8}", f"background_color={bg_bgra}", content
    )
    with open(path, "w") as f:
        f.write(content)
    logging.info("Updated borders/bordersrc")
    restart_borders()
    return True


def restart_borders():
    subprocess.run(["pkill", "-x", "borders"], capture_output=True)
    path = os.path.expanduser("~/.config/borders/bordersrc")
    subprocess.Popen(
        ["bash", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def apply_fastfetch(is_dark_mode):
    path = os.path.expanduser("~/.config/fastfetch/config.jsonc")
    if not os.path.isfile(path):
        return False
    ansi_map = {
        "38;5;111": "38;5;31",
        "38;5;147": "38;5;69",
        "38;5;182": "38;5;93",
        "38;5;114": "38;5;71",
        "38;5;211": "38;5;160",
        "38;5;209": "38;5;202",
        "38;5;221": "38;5;178",
        "38;5;116": "38;5;30",
        "38;5;117": "38;5;39",
    }
    lookup = ansi_map if not is_dark_mode else {v: k for k, v in ansi_map.items()}
    with open(path) as f:
        content = f.read()
    changed = False
    for old, new in lookup.items():
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        with open(path, "w") as f:
            f.write(content)
        logging.info("Updated fastfetch/config.jsonc")
    return changed


def apply_nvim_kickstart(is_dark_mode):
    path = os.path.expanduser("~/.config/nvim-kickstart/init.lua")
    if not os.path.isfile(path):
        return False
    with open(path) as f:
        content = f.read()
    target_line = "  vim.cmd.colorscheme 'catppuccin'"
    setup_line = "  require('catppuccin').setup({ flavour = \"latte\" })"
    has_setup = setup_line in content
    needs_setup = not is_dark_mode and not has_setup
    needs_remove = is_dark_mode and has_setup
    changed = False
    if needs_setup:
        content = content.replace(target_line, f"{setup_line}\n{target_line}")
        changed = True
    elif needs_remove:
        content = content.replace(f"{setup_line}\n", "")
        changed = True
    if changed:
        with open(path, "w") as f:
            f.write(content)
        logging.info("Updated nvim-kickstart/init.lua")
    return changed


def reload_tool(reload_cmd):
    if not reload_cmd:
        return
    logging.info(f"Reload: {reload_cmd}")
    subprocess.Popen(
        ["bash", "-c", reload_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def apply_theme(is_dark_mode):
    mode = "DARK" if is_dark_mode else "LIGHT"
    logging.info(f"Applying {mode} theme")
    for tool in mapping["tools"]:
        name = tool["name"]
        t = tool["type"]
        try:
            if t == "line":
                apply_to_file(tool["file"], tool["replacements"], is_dark_mode)
            elif t == "sketchybar_palette":
                apply_sketchybar(is_dark_mode)
            elif t == "sketchybar_color":
                apply_borders(is_dark_mode)
            elif t == "ansi_replace":
                apply_fastfetch(is_dark_mode)
            elif t == "lua_ks":
                apply_nvim_kickstart(is_dark_mode)
            reload_tool(tool.get("reload"))
        except Exception as e:
            logging.error(f"Error applying {name}: {e}")
    msg = "Light Mode — Catppuccin Latte" if not is_dark_mode else "Dark Mode — Catppuccin Mocha"
    subprocess.run(["osascript", "-e",
        f'display notification "{msg}" with title "Theme Daemon"'],
        capture_output=True)


def daemon_loop():
    current = is_dark()
    apply_theme(current)
    while True:
        time.sleep(2)
        try:
            new = is_dark()
            if new != current:
                current = new
                apply_theme(current)
        except Exception as e:
            logging.error(f"Poll error: {e}")


def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "once":
            load()
            apply_theme(is_dark())
            return
        elif cmd == "pid":
            print(open(PID_FILE).read().strip() if os.path.isfile(PID_FILE) else "")
            return
        print(f"Usage: {sys.argv[0]} [once]", file=sys.stderr)
        sys.exit(1)

    signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))
    signal.signal(signal.SIGINT, lambda *a: sys.exit(0))
    load()
    daemon_loop()


if __name__ == "__main__":
    main()

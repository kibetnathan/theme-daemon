import json
import os
import subprocess

from loguru import logger

from engine.port import ToolPlugin


MANAGER = os.path.expanduser("~/.config/.manager")


class WallpaperPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "wallpaper"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        config_path = os.path.join(MANAGER, "wallpaper.json")
        if not os.path.isfile(config_path):
            logger.warning("wallpaper.json not found")
            return False

        with open(config_path) as f:
            config = json.load(f)

        key = "dark" if is_dark else "light"
        path = os.path.expanduser(config.get(key, ""))
        if not path:
            logger.warning(f"No wallpaper path for {key} mode")
            return False

        script = (
            f'tell application "System Events"\n'
            f"    repeat with d in (every desktop)\n"
            f'        set picture of d to POSIX file "{path}"\n'
            f"    end repeat\n"
            "end tell"
        )
        r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

        if r.returncode != 0:
            logger.error(f"Wallpaper failed: {r.stderr.strip()}")
            return False

        logger.info(f"Wallpaper set to {path}")
        return True

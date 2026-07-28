import json
import os
import subprocess

from loguru import logger

from engine.port import ToolPlugin


class WallpaperPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "wallpaper"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "wallpaper.json")
        config_path = os.path.normpath(config_path)
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

        script = os.path.join(os.path.dirname(__file__), "set-wallpaper.sh")
        r = subprocess.run(["bash", script, path], capture_output=True, text=True, check=False)

        if r.returncode != 0:
            logger.error(f"Wallpaper failed: {r.stderr.strip()}")
            return False

        logger.info(f"Wallpaper set to {path}")
        return True

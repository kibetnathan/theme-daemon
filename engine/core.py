import json
import logging
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from .port import ToolPlugin

MANAGER = os.path.expanduser("~/.config/.manager")


class ThemeEngine:
    def __init__(self):
        self.plugins: list[ToolPlugin] = []
        self.palettes: dict[str, dict] = {}
        self._current_dark: bool | None = None

    def register(self, plugin: ToolPlugin) -> None:
        self.plugins.append(plugin)
        logging.info(f"Registered plugin: {plugin.name}")

    def load_palettes(self) -> None:
        for name in ("mocha", "latte"):
            path = Path(MANAGER) / f"palette-{name}.json"
            self.palettes[name] = json.load(open(path))

    def detect(self) -> bool:
        r = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True, text=True,
        )
        return r.stdout.strip() == "Dark"

    def apply_all(self, is_dark: bool) -> None:
        mode = "DARK" if is_dark else "LIGHT"
        logging.info(f"Applying {mode} theme")
        palette = self.palettes["mocha" if is_dark else "latte"]
        for plugin in self.plugins:
            try:
                if plugin.apply(palette, is_dark):
                    plugin.reload()
            except Exception as e:
                logging.error(f"{plugin.name}: {e}")
        msg = "Light Mode — Catppuccin Latte" if not is_dark else "Dark Mode — Catppuccin Mocha"
        subprocess.run(
            ["osascript", "-e", f'display notification "{msg}" with title "Theme Daemon"'],
            capture_output=True,
        )

    def run(self) -> None:
        signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))
        signal.signal(signal.SIGINT, lambda *a: sys.exit(0))
        self.load_palettes()
        self._current_dark = self.detect()
        self.apply_all(self._current_dark)
        while True:
            time.sleep(2)
            try:
                new = self.detect()
                if new != self._current_dark:
                    self._current_dark = new
                    self.apply_all(new)
            except Exception as e:
                logging.error(f"Poll error: {e}")

    def run_once(self) -> None:
        self.load_palettes()
        self.apply_all(self.detect())

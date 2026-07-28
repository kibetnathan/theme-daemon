import logging
import os

from engine.port import ToolPlugin

ANSI_MAP = {
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


class FastfetchPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "fastfetch"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        path = os.path.expanduser("~/.config/fastfetch/config.jsonc")
        if not os.path.isfile(path):
            return False
        with open(path) as f:
            content = f.read()
        lookup = ANSI_MAP if not is_dark else {v: k for k, v in ANSI_MAP.items()}
        changed = False
        for old, new in lookup.items():
            if old in content:
                content = content.replace(old, new)
                changed = True
        if changed:
            with open(path, "w") as f:
                f.write(content)
            logging.info(f"Updated {path}")
        return changed

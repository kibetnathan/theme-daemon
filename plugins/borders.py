import os
import re

from loguru import logger

from engine.port import ToolPlugin
from ._base import restart_borders_process


class BordersPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "borders"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        path = os.path.expanduser("~/.config/borders/bordersrc")
        if not os.path.isfile(path):
            return False
        with open(path) as f:
            content = f.read()

        for color_key, alpha in [("mauve", "ff"), ("lavender", "dd"), ("mantle", "60")]:
            rgb = palette[color_key]
            argb = f"0x{alpha}{rgb}"
            name = {"mauve": "active", "lavender": "inactive", "mantle": "background"}[color_key]
            content = re.sub(rf"{name}_color=0x[0-9a-fA-F]{{8}}", f"{name}_color={argb}", content)

        with open(path, "w") as f:
            f.write(content)
        logger.info(f"Updated {path}")
        restart_borders_process()
        return True

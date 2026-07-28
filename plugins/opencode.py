import os

from engine.port import ToolPlugin

from ._base import line_replace

TUI_PATH = os.path.expanduser("~/.config/opencode/tui.json")


class OpencodePlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "opencode"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return line_replace(TUI_PATH, [
            ('"catppuccin-mocha"', '"catppuccin-mocha"', '"catppuccin-latte"'),
            ('"catppuccin-latte"', '"catppuccin-mocha"', '"catppuccin-latte"'),
        ], is_dark)

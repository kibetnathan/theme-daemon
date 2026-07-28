from engine.port import ToolPlugin

from ._base import line_replace


class GhosttyPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "ghostty"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        c = "~/.config/ghostty/config"
        a = line_replace(c, [
            ("theme = Catppuccin Mocha",
             "theme = Catppuccin Mocha",
             "theme = Catppuccin Latte"),
        ], is_dark)
        b = line_replace(c, [
            ("background-opacity = 0.66" if is_dark else "background-opacity = 0.85",
             "background-opacity = 0.66",
             "background-opacity = 0.85"),
        ], is_dark)
        return a or b

from engine.port import ToolPlugin

from ._base import line_replace


class BtopPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "btop"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return line_replace(
            "~/.config/btop/btop.conf",
            [('color_theme = "catppuccin-mocha"',
              'color_theme = "catppuccin-mocha"',
              'color_theme = "catppuccin-latte"')],
            is_dark,
        )

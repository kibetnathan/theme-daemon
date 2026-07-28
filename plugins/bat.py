from engine.port import ToolPlugin
from ._base import line_replace


class BatPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "bat"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return line_replace(
            "~/.config/bat/config",
            [('--theme="Catppuccin Mocha"',
              '--theme="Catppuccin Mocha"',
              '--theme="Catppuccin Latte"')],
            is_dark,
        )

from engine.port import ToolPlugin
from ._base import line_replace


class BatPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "bat"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        target = '--theme="Catppuccin Mocha"' if is_dark else '--theme="Catppuccin Latte"'
        return line_replace(
            "~/.config/bat/config",
            [
                ('--theme="Catppuccin Mocha"', target, target),
                ('--theme="Catppuccin Latte"', target, target),
            ],
            is_dark,
        )

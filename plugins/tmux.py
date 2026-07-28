from engine.port import ToolPlugin
from ._base import line_replace, shell


class TmuxPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "tmux"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return line_replace(
            "~/.config/tmux/tmux.conf",
            [('set -g @ukiyo-theme "catppuccin/mocha"',
              'set -g @ukiyo-theme "catppuccin/mocha"',
              'set -g @ukiyo-theme "catppuccin/latte"')],
            is_dark,
        )

    def reload(self) -> None:
        shell("tmux source-file ~/.config/tmux/tmux.conf")

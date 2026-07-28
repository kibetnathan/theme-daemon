import os

from engine.port import ToolPlugin

from ._base import line_replace, shell

TMUX_CONF = os.path.expanduser("~/.config/tmux/tmux.conf")


class TmuxPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "tmux"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return line_replace(TMUX_CONF, [
            ("@catppuccin_flavor 'mocha'", "@catppuccin_flavor 'mocha'", "@catppuccin_flavor 'latte'"),
            ("@catppuccin_flavor 'latte'", "@catppuccin_flavor 'mocha'", "@catppuccin_flavor 'latte'"),
        ], is_dark)

    def reload(self) -> None:
        shell("tmux source-file ~/.config/tmux/tmux.conf")

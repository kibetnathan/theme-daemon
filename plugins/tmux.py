import os
import re

from engine.port import ToolPlugin
from ._base import shell


class TmuxPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "tmux"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        path = os.path.expanduser("~/.config/tmux/tmux.conf")
        if not os.path.isfile(path):
            return False
        with open(path) as f:
            content = f.read()
        target = "mocha" if is_dark else "latte"
        new, n = re.subn(
            r'(set -g @ukiyo-theme "catppuccin/)(mocha|latte)(")',
            rf'\g<1>{target}\g<3>',
            content,
        )
        if n == 0:
            return False
        with open(path, "w") as f:
            f.write(new)
        return True

    def reload(self) -> None:
        shell("tmux source-file ~/.config/tmux/tmux.conf")

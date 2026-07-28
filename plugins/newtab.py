from engine.port import ToolPlugin
from ._base import line_replace


class NewtabPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "newtab"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return line_replace(
            "~/.config/newtab/newtab.html",
            [("background: #0d0d0d",
              "        background: #0d0d0d;",
              "        background: #eff1f5;")],
            is_dark,
        )

from engine.port import ToolPlugin
from ._base import palette_rewrite, shell


class SketchybarPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "sketchybar"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return palette_rewrite("~/.config/sketchybar/colors.sh", palette)

    def reload(self) -> None:
        shell("sketchybar --reload")

from engine.port import ToolPlugin
from ._base import line_replace, shell


DARK = "                                        insert_feedback_color 0xffa6e3a1 \\"
LIGHT = "                                        insert_feedback_color 0xff40a02b \\"


class YabaiPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "yabai"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        target = DARK if is_dark else LIGHT
        return line_replace(
            "~/.config/yabai/yabairc",
            [(DARK, target, target), (LIGHT, target, target)],
            is_dark,
        )

    def reload(self) -> None:
        shell("yabai --restart-service")

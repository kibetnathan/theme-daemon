from engine.port import ToolPlugin
from ._base import line_replace, shell


class YabaiPlugin(ToolPlugin):
    @property
    def name(self) -> str:
        return "yabai"

    def apply(self, palette: dict, is_dark: bool) -> bool:
        return line_replace(
            "~/.config/yabai/yabairc",
            [("insert_feedback_color 0xffa6e3a1",
              "  insert_feedback_color 0xffa6e3a1 \\",
              "  insert_feedback_color 0xff40a02b \\")],
            is_dark,
        )

    def reload(self) -> None:
        shell("yabai --restart-service")

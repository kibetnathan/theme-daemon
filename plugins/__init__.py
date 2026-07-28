from .bat import BatPlugin
from .borders import BordersPlugin
from .btop import BtopPlugin
from .fastfetch import FastfetchPlugin
from .ghostty import GhosttyPlugin
from .newtab import NewtabPlugin
from .sketchybar import SketchybarPlugin
from .tmux import TmuxPlugin
from .wallpaper import WallpaperPlugin
from .yabai import YabaiPlugin


def all_plugins():
    return [
        BatPlugin(),
        GhosttyPlugin(),
        BtopPlugin(),
        TmuxPlugin(),
        BordersPlugin(),
        SketchybarPlugin(),
        FastfetchPlugin(),
        NewtabPlugin(),
        YabaiPlugin(),
        WallpaperPlugin(),
    ]

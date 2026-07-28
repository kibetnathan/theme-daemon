from .bat import BatPlugin
from .ghostty import GhosttyPlugin
from .btop import BtopPlugin
from .tmux import TmuxPlugin
from .borders import BordersPlugin
from .sketchybar import SketchybarPlugin
from .fastfetch import FastfetchPlugin
from .newtab import NewtabPlugin
from .yabai import YabaiPlugin
from .wallpaper import WallpaperPlugin


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

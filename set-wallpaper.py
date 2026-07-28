import os
import plistlib
import subprocess

WALLPAPER_PATH = os.path.expanduser(os.environ.get("WALLPAPER_PATH", ""))
PLIST_PATH = os.path.expanduser(
    "~/Library/Application Support/com.apple.wallpaper/Store/Index.plist"
)
CACHE_PATH = os.path.expanduser(
    "~/Library/Containers/com.apple.wallpaper.extension.image/Data/Library/Preferences/com.apple.wallpaper.extension.image.plist"
)


def update_choices(choices, url_value):
    for choice in choices:
        cfg = choice.get("Configuration")
        if cfg:
            inner = plistlib.loads(cfg)
            if "url" in inner:
                inner["url"] = {"relative": url_value}
                choice["Configuration"] = plistlib.dumps(inner)


with open(PLIST_PATH, "rb") as f:
    data = plistlib.load(f)

url_value = f"file://{WALLPAPER_PATH}"

for section_key in ("SystemDefault",):
    section = data.get(section_key, {})
    for mode_key in ("Desktop", "Idle"):
        mode = section.get(mode_key, {})
        if "Content" in mode:
            update_choices(mode["Content"].get("Choices", []), url_value)

for display in data.get("Displays", {}).values():
    for mode_key in ("Desktop", "Idle"):
        mode = display.get(mode_key, {})
        if "Content" in mode:
            update_choices(mode["Content"].get("Choices", []), url_value)

for space in data.get("Spaces", {}).values():
    default = space.get("Default", {})
    for link_key in ("Desktop", "Linked", "Idle"):
        link = default.get(link_key, {})
        if "Content" in link:
            update_choices(link["Content"].get("Choices", []), url_value)

all_entry = data.get("AllSpacesAndDisplays", {})
for mode_key in ("Desktop", "Idle"):
    mode = all_entry.get(mode_key, {})
    if "Content" in mode:
        update_choices(mode["Content"].get("Choices", []), url_value)

with open(PLIST_PATH, "wb") as f:
    plistlib.dump(data, f, fmt=plistlib.FMT_BINARY)

if os.path.isfile(CACHE_PATH):
    with open(CACHE_PATH, "rb") as f:
        cache = plistlib.load(f)
    cache["ChoiceRequests.ImageFiles"] = []
    with open(CACHE_PATH, "wb") as f:
        plistlib.dump(cache, f, fmt=plistlib.FMT_BINARY)

subprocess.run(["pkill", "-x", "WallpaperImageE"], capture_output=True)

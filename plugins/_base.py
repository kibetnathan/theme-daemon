import os
import re
import subprocess

from loguru import logger


def line_replace(path: str, replacements: list[tuple[str, str, str]], is_dark: bool) -> bool:
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        logger.warning(f"File not found: {path}")
        return False
    with open(path) as f:
        content = f.read()
    changed = False
    for search, dark_val, light_val in replacements:
        target = dark_val if is_dark else light_val
        if search in content:
            new = content.replace(search, target, 1)
            if new != content:
                content = new
                changed = True
    if changed:
        with open(path, "w") as f:
            f.write(content)
        logger.info(f"Updated {path}")
    return changed


def palette_rewrite(path: str, palette: dict) -> bool:
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        logger.warning(f"File not found: {path}")
        return False
    with open(path) as f:
        content = f.read()

    def replace_color(m):
        var = m.group(1)
        key = var.lower()
        if key in palette:
            return f"export {var}=0xff{palette[key]}"
        return m.group(0)

    new_content = re.sub(
        r"^export (\w+)=0x[0-9a-fA-F]{8}",
        replace_color, content, flags=re.MULTILINE,
    )
    if new_content != content:
        with open(path, "w") as f:
            f.write(new_content)
        logger.info(f"Updated {path}")
        return True
    return False


def restart_borders_process() -> None:
    subprocess.run(["pkill", "-x", "borders"], capture_output=True)
    path = os.path.expanduser("~/.config/borders/bordersrc")
    subprocess.Popen(["bash", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def shell(reload_cmd: str) -> None:
    logger.info(f"Reload: {reload_cmd}")
    subprocess.Popen(["bash", "-c", reload_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

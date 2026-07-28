#!/usr/bin/env python3
from plugins import all_plugins
from engine.core import ThemeEngine
from loguru import logger
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


LOG_DIR = os.path.expanduser("~/.config/.manager/cache/theme-daemon/logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()
logger.add(
    os.path.join(LOG_DIR, "theme-daemon-{time:YYYY-MM-DD}.log"),
    rotation="10 MB",
    retention="7 days",
    format="{time:HH:mm:ss} {message}",
    level="INFO",
)


def main():
    engine = ThemeEngine()
    for plugin in all_plugins():
        engine.register(plugin)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "once":
            engine.run_once()
            return
        elif cmd == "pid":
            pid_file = "/tmp/theme-daemon.pid"
            if os.path.isfile(pid_file):
                print(open(pid_file).read().strip())
            return
        elif cmd == "logs":
            import glob

            logs = sorted(glob.glob(os.path.join(LOG_DIR, "*.log")))
            print("\n".join(logs) if logs else "no logs")
            return
        print(f"Usage: {sys.argv[0]} [once|logs]", file=sys.stderr)
        sys.exit(1)

    engine.run()


if __name__ == "__main__":
    main()

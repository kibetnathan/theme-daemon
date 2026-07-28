#!/usr/bin/env python3
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LOG_FILE = "/tmp/theme-daemon.log"
logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO,
    format="%(asctime)s %(message)s", datefmt="%H:%M:%S",
)

from engine.core import ThemeEngine
from plugins import all_plugins


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
        print(f"Usage: {sys.argv[0]} [once]", file=sys.stderr)
        sys.exit(1)

    engine.run()


if __name__ == "__main__":
    main()

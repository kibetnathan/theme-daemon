#!/bin/bash
DAEMON="$HOME/.config/.manager/theme-daemon.py"
PID_FILE="/tmp/theme-daemon.pid"
LOG_FILE="/tmp/theme-daemon.log"

start() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "theme-daemon already running (pid $(cat "$PID_FILE"))"
    return 1
  fi
  nohup python3 "$DAEMON" >> "$LOG_FILE" 2>&1 &
  PID=$!
  echo $PID > "$PID_FILE"
  echo "theme-daemon started (pid $PID)"
}

stop() {
  if [ ! -f "$PID_FILE" ]; then
    echo "theme-daemon not running"
    return 1
  fi
  PID=$(cat "$PID_FILE")
  kill "$PID" 2>/dev/null
  rm -f "$PID_FILE"
  echo "theme-daemon stopped"
}

status() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "running (pid $(cat "$PID_FILE"))"
  else
    echo "stopped"
    [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
  fi
}

case "${1:-}" in
  start)   start ;;
  stop)    stop ;;
  status)  status ;;
  once)    python3 "$DAEMON" once ;;
  restart) stop; sleep 0.5; start ;;
  *)
    echo "Usage: $0 {start|stop|status|restart|once}"
    exit 1
    ;;
esac

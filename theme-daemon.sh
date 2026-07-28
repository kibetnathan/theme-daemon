#!/bin/bash
DAEMON="$HOME/.config/.manager/theme-daemon.py"
PID_FILE="/tmp/theme-daemon.pid"
LOG_DIR="$HOME/.config/.manager/cache/theme-daemon/logs"

start() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "theme-daemon already running (pid $(cat "$PID_FILE"))"
    return 1
  fi
  nohup python3 "$DAEMON" >> /dev/null 2>&1 &
  PID=$!
  echo $PID > "$PID_FILE"
  echo "theme-daemon started (pid $PID)"
  echo "logs: $LOG_DIR"
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

logs() {
  local logfile=$(ls -t "$LOG_DIR"/*.log 2>/dev/null | head -1)
  if [ -z "$logfile" ]; then
    echo "no logs found"
    return 1
  fi
  case "${2:-}" in
    tail|follow) tail -f "$logfile" ;;
    last) tail -20 "$logfile" ;;
    *) less "$logfile" ;;
  esac
}

case "${1:-}" in
  start)   start ;;
  stop)    stop ;;
  status)  status ;;
  restart) stop; sleep 0.5; start ;;
  once)    python3 "$DAEMON" once ;;
  logs)    logs "$@" ;;
  *)
    echo "Usage: $0 {start|stop|status|restart|once|logs [tail|last]}"
    exit 1
    ;;
esac

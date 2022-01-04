#!/bin/sh

while [ $# -gt 0 ]; do
  case "$1" in
    --net*|-n*)
      if [[ "$1" != *=* ]]; then shift; fi
      net="${1#*=}"
      ;;
    --led*|-l*)
      if [[ "$1" != *=* ]]; then shift; fi
      led="${1#*=}"
      ;;
    *)
      >&2 printf "Unrecognised argument ${1}\n"
      >&2 printf "Usage: upload.sh --net <*.py> --led <*.py>\n"
      exit 1
      ;;
  esac
  shift
done

if [ -z ${net} ]; then
    >&2 printf "Usage: upload.sh --net <*.py> --led <*.py>\n"
    exit 1
fi

if [ -z ${led} ]; then
    >&2 printf "Usage: upload.sh --net <*.py> --led <*.py>\n"
    exit 1
fi

for file in *.py; do
    printf "Uploading ${file}\n"
    ampy --port /dev/ttyUSB0 --baud 115200 put $file
done

printf "Uploading ${net} as 'setup_net.py'\n"
ampy --port /dev/ttyUSB0 --baud 115200 put $net setup_net.py

printf "Uploading ${led} as 'setup_led.py'\n"
ampy --port /dev/ttyUSB0 --baud 115200 put $led setup_led.py


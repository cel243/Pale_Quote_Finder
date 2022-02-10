#!/usr/bin/env bash 

if [[ $# -lt 1 ]]; then
  echo "requires regex"
fi

echo " "

export GREP_COLOR='1;36;40'

./describe_all.sh \
  | egrep --color=none -i "$1" \
  | egrep --color=always "^[0-9\(\) A-Za-z\.]*:"\
  | awk '{ print $0, "\n"}'

echo " "



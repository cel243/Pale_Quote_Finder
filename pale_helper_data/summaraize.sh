#!/usr/bin/env bash 

if [[ $# -lt 1 ]]; then
  echo "requires regex"
fi

echo " "

export GREP_COLOR='1;36;40'

/Users/carolinelui/Desktop/pale/pale_helper_data/chapter_summaries.sh \
  | egrep --color=none -i "$1" \
  | egrep --color=always "^[^:]*:"\
  | awk '{ print $0, "\n"}'

echo " "



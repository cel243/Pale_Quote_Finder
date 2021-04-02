#!/usr/bin/env bash 

if [[ $# -lt 1 ]]; then
  echo "requires regex"
  echo "usage: search_pale regex file_match flags"
  exit
fi

export GREP_COLOR='1;36;40'
cd Pale_Chapters/

egrep --color=always -r$3  "$1" ./$2 | grep --color=always ".*txt" | sort | awk '{ print $0, "\n"}'

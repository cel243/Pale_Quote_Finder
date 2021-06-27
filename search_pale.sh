#!/usr/bin/env bash 

if [[ $# -lt 1 ]]; then
  echo "requires regex"
  echo "usage: search_pale regex [flags] [file_match] [file_constraint] [constraint_flags]"
  exit
fi

## ./search_pale "regex" files_to_search flags file_constraint constraint_flags

export GREP_COLOR='1;36;40'
cd Pale_Chapters/

if [[ $# -gt 3 ]]; then
  while IFS= read -r file; do
      # echo $dir
      egrep --color=always -r$2  "$1" "$file" | grep "txt.." | grep --color=always ".*txt" | awk '{ print $0, "\n"}'
  done < <(egrep -rl$5 "$4" ./$3 | sort )
else
  egrep --color=always -r$2  "$1" ./$3 | grep --color=always ".*txt" | sort -s -k 1,1 | awk '{ print $0, "\n"}'
fi

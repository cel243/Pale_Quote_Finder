#!/usr/bin/env bash 

if [[ $# -lt 1 ]]; then
  echo "requires regex"
  echo "usage: search_pale regex [flags] [file_match] [file_constraint] [constraint_flags]"
  exit
fi

export GREP_COLOR='1;36;40'
cd Pale_Chapters/

if [[ $# -gt 3 ]]; then
  while IFS= read -r file; do
    if [[ "$2" == *l* ]]; then
      flags=$( sed 's/l//' <<< "$2" )
      if grep -q -E -r$flags  "$1" "$file"; then 
        grep --color=always ".*txt" <<< "$file"
        echo " "
      fi
    else
      egrep --color=always -r$2  "$1" "$file" | grep "txt.." | grep --color=always ".*txt" | awk '{ print $0, "\n"}'
    fi
  done < <( eval "egrep -rl$5 \"$4\" ./$3" | sort )
else
  if [[ "$2" == *l* ]]; then
    eval "egrep --color=always -r$2  \"$1\" ./$3" \
      | grep --color=always ".*txt" \
      | sort -s -k 1,1 \
      | awk '{ print $0, "\n"}'
  else
    eval "egrep --color=always -r$2  \"$1\" ./$3" \
      | grep "txt.." \
      | grep --color=always ".*txt" \
      | sort -s -k 1,1 \
      | awk '{ print $0, "\n"}'
  fi
fi

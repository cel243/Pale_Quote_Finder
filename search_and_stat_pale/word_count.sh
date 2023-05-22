
if [[ $# -eq 1 ]]; then

arc=0
if [[ $1 -lt 10 ]]; then 
  arc="0$1"
else 
  arc="$1"
fi

echo " "
echo "---CHAP---|---WORDS---|"
echo "----------|-----------|"
arc_total=0
for chapter in Pale_Chapters/$arc/*
do
  printf "   "
  printf $( egrep -o "$1\.[a-zA-Z0-9]+" <<< $chapter  )
  chap_num=$( egrep -o  "\.[a-zA-Z0-9]+" <<< $chapter | grep -v "txt" )
  if [[ ${#chap_num} -lt 3 ]]; then 
    printf " "
  fi
  if [[ $1 -lt 10 ]]; then
    printf " "
  fi
  printf "  |  "
  chapter_total=$( cat "${chapter}" | wc -w )
  arc_total=$(( $arc_total + $chapter_total ));
  echo $chapter_total
done

echo "----------------------"
echo "ARC TOTAL: $arc_total"
echo " "

else

echo " "
echo "-ARC-|-CHAPS-|---WORDS----|"
echo "-----|-------|------------|"
pale_total=0
pale_chap_total=0
arc_total=0
arc_chap_total=0
for dir in Pale_Chapters/*; do
  arc=$( echo "${dir}" | ggrep -oP "(?<=Pale_Chapters.).*" )
  arc_total=0
  arc_chap_total=0
  printf " "
  printf "${arc}  |  "
  for chapter in $dir/*; do
    chapter_total=$( cat "${chapter}" | wc -w )
    arc_total=$(( $arc_total + $chapter_total ));
    arc_chap_total=$(( $arc_chap_total + 1 ));
      if [[ $line != "EM" ]]; then 
        pale_chap_total=$(( $pale_chap_total + 1 ));
      fi 
  done
  if [[ $arc_chap_total -lt 10 ]]; then
  echo "$arc_chap_total    |  $arc_total";
  else 
  echo "$arc_chap_total   |  $arc_total";
  fi 
  if [[ $line != "EM" ]]; then 
    pale_total=$(( $pale_total + $arc_total ));
  fi 
done
echo "--------------------------------------"
echo "STORY WORDS: $pale_total (word count without EM)"
echo "TOTAL WORDS: $(( $pale_total + $arc_total ))"
echo "TOTAL CHAPTERS: $pale_chap_total"
echo " "

fi 

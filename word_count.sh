
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
while IFS= read -r chapter; do
  echo -n "   "
  echo -n $( egrep -o "$1\.[a-z0-9]+" <<< $chapter  )
  chap_num=$( egrep -o  "\.[a-z0-9]+" <<< $chapter | grep -v "txt" )
  if [[ ${#chap_num} -lt 3 ]]; then 
    echo -n " "
  fi
  if [[ $1 -lt 10 ]]; then
    echo -n " "
  fi
  echo -n "  |  "
  chapter_total=$( cat Pale_Chapters/"$arc"/"$chapter" | wc -w )
  arc_total=$(( $arc_total + $chapter_total ));
  echo $chapter_total
done < <( ls Pale_Chapters/"$arc"/ | sort )
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
while IFS= read -r line; do
  arc_total=0
  arc_chap_total=0
  echo -n " "
  echo -n "$line  |  "
  while IFS= read -r chapter; do
    chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
    arc_total=$(( $arc_total + $chapter_total ));
    arc_chap_total=$(( $arc_chap_total + 1 ));
      if [[ $line != "EM" ]]; then 
        pale_chap_total=$(( $pale_chap_total + 1 ));
      fi 
  done < <( ls Pale_Chapters/"$line" )
  if [[ $arc_chap_total -lt 10 ]]; then
  echo "$arc_chap_total    |  $arc_total";
  else 
  echo "$arc_chap_total   |  $arc_total";
  fi 
  if [[ $line != "EM" ]]; then 
    pale_total=$(( $pale_total + $arc_total ));
  fi 
done < <( ls Pale_Chapters/ )
echo "--------------------------------------"
echo "STORY WORDS: $pale_total (word count without EM)"
echo "TOTAL WORDS: $(( $pale_total + $arc_total ))"
echo "TOTAL CHAPTERS: $pale_chap_total"
echo " "

fi 

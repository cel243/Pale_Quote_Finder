
if [[ $# -eq 1 ]]; then

echo " "
echo "---ARC---|---WORDS---|"
echo "---------|-----------|"
arc_total=0
while IFS= read -r chapter; do
  echo -n "  "
  echo -n $( egrep -o "$1\.[a-z0-9]+" <<< $chapter  )
  chap_num=$( egrep -o  "\.[a-z0-9]+" <<< $chapter | grep -v "txt" )
  if [[ ${#chap_num} -lt 3 ]]; then 
    echo -n " "
  fi
  echo -n "  |  "
  chapter_total=$( cat Pale_Chapters/$1/"$chapter" | wc -w )
  arc_total=$(( $arc_total + $chapter_total ));
  echo $chapter_total
done < <( ls Pale_Chapters/$1/ )
echo "----------------------"
echo "ARC TOTAL: $arc_total"
echo " "

else

echo " "
echo "-ARC-|--WORDS-----|"
echo "-----|------------|"
pale_total=0
while IFS= read -r line; do
  arc_total=0;
  echo -n " "
  echo -n "$line  |  "
  while IFS= read -r chapter; do
    chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
    arc_total=$(( $arc_total + $chapter_total ));
  done < <( ls Pale_Chapters/"$line" )
  echo $arc_total
  pale_total=$(( $pale_total + $arc_total ))
done < <( ls Pale_Chapters/ )
echo "-----------------------"
echo "TOTAL WORDS: $pale_total"
echo " "

fi 

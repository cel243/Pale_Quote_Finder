
all_counts=""
for line in Pale_Chapters/*; do
  for chapter in $line/*; do
    chapter_total=$( cat "${chapter}" | wc -w )
    echo "$chapter_total -- $chapter"
  done
done 


all_counts=""
while IFS= read -r line; do

  while IFS= read -r chapter; do
    chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
    echo "$chapter_total -- $chapter"
  done < <( ls Pale_Chapters/"$line" )

done < <( ls Pale_Chapters/ )


echo ""
lucy_total=0
verona_total=0
avery_total=0
int_total=0

while IFS= read -r line; do
  while IFS= read -r chapter; do
    if [[ "$chapter" == *"Lucy"* ]]; then
      # echo "$chapter"
      chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
      lucy_total=$(( $lucy_total + $chapter_total ));
    fi
    if [[ "$chapter" == *"Verona"* ]]; then
      # echo "$chapter"
      chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
      verona_total=$(( $verona_total + $chapter_total ));
    fi
    if [[ "$chapter" == *"Avery"* ]]; then
      # echo "$chapter"
      chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
      avery_total=$(( $avery_total + $chapter_total ));
    fi
    if [[ "$chapter" == *"8.8"*"All"* ]]; then
      # echo "$chapter"
      avery_total=$(( $avery_total + 4678 ));
      verona_total=$(( $verona_total + 5282 ));
      lucy_total=$(( $lucy_total + 2956 ));
      int_total=$(( $int_total + 947 ));
    fi
    if [[ "$chapter" == *"11.13"*"All"* ]]; then
      # echo "$chapter"
      avery_total=$(( $avery_total + 2185 ));
      verona_total=$(( $verona_total +  3848 ));
      lucy_total=$(( $lucy_total + 7141 ));
    fi
    if [[ "$chapter" == *Interlude* ]]; then
      # echo "$chapter"
      chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
      int_total=$(( $int_total + $chapter_total ));
    fi
    if [[ "$chapter" == *Prologue* ]]; then
      # echo "$chapter"
      chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
      int_total=$(( $int_total + $chapter_total ));
    fi
  done < <( ls Pale_Chapters/"$line" )
done < <( ls Pale_Chapters/ )

echo "----- CHAPTERS ---- WORDS ----"
echo "----|----------|-------------"
echo -n " L: |    "
echo -n $(( $( grep -rl " " ./Pale_Chapters/[01][0-9]/*Lucy* | wc -l ) + 2 ))
echo -n "    |   "
echo "$lucy_total"

echo -n " V: |    "
echo -n $(( $( grep -rl " " ./Pale_Chapters/[01][0-9]/*Verona* | wc -l ) + 2 ))
echo -n "    |   "
echo "$verona_total"

echo -n " A: |    "
echo -n $(( $( grep -rl " " ./Pale_Chapters/[01][0-9]/*Avery* | wc -l ) + 2 ))
echo -n "    |   "
echo "$avery_total"

echo -n " I: |    "
echo -n $(( $( grep -rl " " ./Pale_Chapters/[01][0-9]/*Interlude*.txt | wc -l ) + 1 ))
echo -n "    |   "
echo "$int_total"

echo ""
echo "- ARC -- PERSECTIVE CHAP COUNT ------------- PERSPECTIVE WORD COUNT---------"
echo "------|--------------------------||-----------------------------------------"

lucy=0
l_word=0
avery=0
a_word=0
verona=0
v_word=0
interlude=0
i_word=0
while IFS= read -r line; do
  if [[ ( "$line" == *[01][0-9]* ) && ! ( "$line" == *00* ) ]]; then
    while IFS= read -r chapter; do
      chapter_total=$( cat Pale_Chapters/"$line"/"$chapter" | wc -w )
      if [[ "$chapter" == *"Lucy"* ]]; then
        lucy=$(( $lucy + 1 ));
        l_word=$(( $l_word + $chapter_total ))
      fi
      if [[ "$chapter" == *"Verona"* ]]; then
        verona=$(( $verona + 1 ));
        v_word=$(( $v_word + $chapter_total ))
      fi
      if [[ "$chapter" == *"Avery"* ]]; then
        avery=$(( $avery + 1 ));
        a_word=$(( $a_word + $chapter_total ))
      fi
      if [[ "$chapter" == *"8.8"*"All"* ]]; then
        avery=$(( $avery + 1 ));
        verona=$(( $verona + 1 ));
        lucy=$(( $lucy + 1 ));
        a_word=$(( $a_word + 4678 ))
        v_word=$(( $v_word + 5282 ))
        l_word=$(( $l_word + 2956 ))
        i_word=$(( $i_word + 947 ))
      fi
      if [[ "$chapter" == *"11.13"*"All"* ]]; then
        avery=$(( $avery + 1 ));
        verona=$(( $verona + 1 ));
        lucy=$(( $lucy + 1 ));
        a_word=$(( $a_word + 2185 ))
        v_word=$(( $v_word + 3848 ))
        l_word=$(( $l_word + 7141 ))
      fi
      if [[ "$chapter" == *"Interlude"* ]]; then
        interlude=$(( $interlude + 1 ));
        i_word=$(( $i_word + $chapter_total ))
      fi
    done < <( ls Pale_Chapters/"$line" )
    echo "  $line: | L ($lucy) V ($verona) A ($avery) I ($interlude)  ||  L ($l_word) V ($v_word) A ($a_word) I ($i_word) "
    lucy=0
    l_word=0
    avery=0
    a_word=0
    verona=0
    v_word=0
    interlude=0
    i_word=0
  fi
done < <( ls Pale_Chapters/ )

echo " "
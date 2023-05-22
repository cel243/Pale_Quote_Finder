echo ""
global_lucy_total=0
global_verona_total=0
global_avery_total=0
global_int_total=0
global_lucy_chapters=0
global_verona_chapters=0
global_avery_chapters=0
global_interludes=0

arc_lucy_total=0
arc_verona_total=0
arc_avery_total=0
arc_int_total=0
arc_lucy_chapters=0
arc_verona_chapters=0
arc_avery_chapters=0
arc_interludes=0

python3 pale_helper_data/print_character_counts.py > tmp.txt 

previous_arc=0

echo ""
echo "- ARC -- PERSECTIVE CHAP COUNT ------------- PERSPECTIVE WORD COUNT---------"
echo "------|--------------------------||-----------------------------------------"

while IFS= read -r line; do
  chapter=$( echo "${line}" | ggrep -oP "^.*(?=\-)" )
  character_word_counts_str=$( echo "${line}" | ggrep -oP "(?<=\-).*(?=;)" )
  IFS=";" read -r -a character_word_counts <<< "${character_word_counts_str}"

  for x in "${character_word_counts[@]}"
  do
    character=$( echo "${x}" | ggrep -oP "^.*(?=,)" )
    count=$( echo "${x}" | ggrep -oP "(?<=,).*" )
    if [[ "${character}" == "lucy" ]]; then
      global_lucy_total=$(( $global_lucy_total + $count ));
      global_lucy_chapters=$(( $global_lucy_chapters + 1 ))
      arc_lucy_total=$(( $arc_lucy_total + $count ));
      arc_lucy_chapters=$(( $arc_lucy_chapters + 1 ))
    elif [[ "${character}" == "verona" ]]; then
      global_verona_total=$(( $global_verona_total + $count ));
      global_verona_chapters=$(( $global_verona_chapters + 1 ))
      arc_verona_total=$(( $arc_verona_total + $count ));
      arc_verona_chapters=$(( $arc_verona_chapters + 1 ))
    elif [[ "${character}" == "avery" ]]; then
      global_avery_total=$(( $global_avery_total + $count ));
      global_avery_chapters=$(( $global_avery_chapters + 1 ))
      arc_avery_total=$(( $arc_avery_total + $count ));
      arc_avery_chapters=$(( $arc_avery_chapters + 1 ))
    else
      global_int_total=$(( $global_int_total + $count ));
      global_interludes=$(( $global_interludes + 1 ))
      arc_int_total=$(( $arc_int_total + $count ));
      arc_interludes=$(( $arc_interludes + 1 ))
    fi
  done

  arc=$( echo "${line}" | ggrep -oP "[0-9]+(?=\.)" )

  if [[ ! "${arc}" == "${previous_arc}" ]]; then
    printf "  %02d: | " $arc
    echo "L ($arc_lucy_chapters) V ($arc_verona_chapters) A ($arc_avery_chapters) I ($arc_interludes)\
    ||  L ($arc_lucy_total) V ($arc_verona_total) A ($arc_avery_total) I ($arc_int_total) "
    arc_lucy_total=0
    arc_verona_total=0
    arc_avery_total=0
    arc_int_total=0
    arc_lucy_chapters=0
    arc_verona_chapters=0
    arc_avery_chapters=0
    arc_interludes=0
  fi
  previous_arc=$arc

done < tmp.txt

echo
echo "----- CHAPTERS ---- WORDS ----"
echo "----|----------|-------------"
echo " L: |    ${global_lucy_chapters}    |   ${global_lucy_total}"
echo " V: |    ${global_verona_chapters}    |   ${global_verona_total}"
echo " A: |    ${global_avery_chapters}    |   ${global_avery_total}"
echo " I: |    ${global_interludes}    |   ${global_int_total}"




if [[ $# -lt 2 ]]; then
  echo "needs arguments"
  exit
fi

if [[ $1 == "em" ]]; then
  open ./Pale_Chapters/EM/*$2.$3*
  exit
fi

if [[ $1 -lt 10 ]]; then
  open ./Pale_Chapters/0$1/*.$2*
  exit
else
  open ./Pale_Chapters/$1/*.$2*
fi

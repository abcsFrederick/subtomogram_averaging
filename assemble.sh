#!/bin/bash

COLUMNS=10
BLANK=blank.mrc

shopt -s nullglob
FILES=(aligned_tom1_P[0-9][0-9][0-9][0-9].mrc)

N="${#FILES[@]}"
if [ "${N}" -eq 0 ]; then
  echo "no aligned particle files found"
  exit 1
fi

FILENAME="${FILES[0]}"

SIZE=($(header -s ${FILENAME}))
ROWS=$((${N} / ${COLUMNS}))
REMAINDER=$((${N} % ${COLUMNS}))

if [ "${REMAINDER}" -ne 0 ]; then
  ROWS=$((${ROWS} + 1));
  EXTRA=$((${COLUMNS} - ${REMAINDER}))
  BLANKS=$(eval "printf \" ${BLANK}\"%.0s {1..$EXTRA}")
  newstack -multadd 0,0 "${FILENAME}" "${BLANK}"
fi

for i in "${!FILES[@]}"; do 
  LABEL=$(echo "${FILES[$i]}" | sed 's/aligned_tom1_P0*\([0-9]*\)\.mrc/\1/')
  Y=$((${ROWS} - ${i}/${COLUMNS} - 1))
  X=$((${i} - ${i}/${COLUMNS}*${COLUMNS}))
  printf "%s,%s,%s\n" "${LABEL}" "${Y}" "${X}"
done | label.py ${SIZE[*]} > assembled.amod

assemblevol -input ${FILES[*]} ${BLANKS} \
            -output assembled.mrc \
	    -nxfiles "${COLUMNS}" -nyfiles "${ROWS}" -nzfiles 1

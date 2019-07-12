#!/bin/bash

PREFIX="${SLURM_JOB_ID:-$(date +%s.%N)}"
N_PROC="${SLURM_CPUS_PER_TASK:-1}"

[ -d "/lscratch/${SLURM_JOB_ID}" ] && export TMPDIR="/lscratch/${SLURM_JOB_ID}"
mkdir -p "${TMPDIR}/${PREFIX}"

echo "using directory ${TMPDIR}/${PREFIX}"
echo

module load PEET
module load python/3.6

echo "1 = $1"
echo "2 = $2"
echo "3 = $3"
echo "ARGS = $*"

# create .prm for processing from CLA
# save remaing arugments for .mrc and .fcsv files for remaining files
ARGS=$((python prm.py \
    --fnVolume "{'${PREFIX}.mrc'}" \
    --fnModParticle "{'${PREFIX}.mod'}" \
    --fnOutput "'${PREFIX}'" \
    --output-unused-arguments \
    $* 1> "${TMPDIR}/${PREFIX}/${PREFIX}.prm") 2>&1) 

echo
echo "${PREFIX}.prm:"
cat "${TMPDIR}/${PREFIX}/${PREFIX}.prm"
echo

VOLUME=$((python fcsv2points.py --output-volume-filename ${ARGS} "${TMPDIR}/${PREFIX}/${PREFIX}.points") 2>&1)
echo "volume: ${VOLUME}"
point2model "${TMPDIR}/${PREFIX}/${PREFIX}.points" "${TMPDIR}/${PREFIX}/${PREFIX}.mod"
python sitk_convert.py "${VOLUME}" "${TMPDIR}/${PREFIX}/${PREFIX}.mrc"

pushd .
cd "${TMPDIR}/${PREFIX}"
prmParser "${PREFIX}.prm"
processchunks -g "localhost:${N_PROC}" "${PREFIX}"
popd

cp -r "${TMPDIR}/${PREFIX}" "PEET-${PREFIX}"

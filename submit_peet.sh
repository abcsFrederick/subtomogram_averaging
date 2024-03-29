#!/bin/bash

PREFIX="${SLURM_JOB_ID:-$(date +%s.%N)}"
N_PROC="${SLURM_CPUS_PER_TASK:-1}"

[ -d "/lscratch/${SLURM_JOB_ID}" ] && export TMPDIR="/lscratch/${SLURM_JOB_ID}"

if [[ -z "${TMPDIR}" ]]; then
    echo "no TMPDIR set"
    exit 1
fi

mkdir -p "${TMPDIR}/${PREFIX}"

if [[ ! -w "${TMPDIR}/${PREFIX}" ]]; then
    echo "${TMPDIR}/${PREFIX} not writable"
    exit 1
fi

echo "using directory ${TMPDIR}/${PREFIX}"
echo

module load PEET
module load python/3.6

echo "ARGS = $*"

# create .prm for processing from CLA
# save remaing arugments for .mrc and .fcsv files for remaining files
ARGS=$((prm.py \
    --fnVolume "{'${PREFIX}.mrc'}" \
    --fnModParticle "{'${PREFIX}.mod'}" \
    --fnOutput "'${PREFIX}'" \
    --output-unused-arguments \
    $* 1> "${TMPDIR}/${PREFIX}/${PREFIX}.prm") 2>&1) 

echo
echo "${PREFIX}.prm:"
cat "${TMPDIR}/${PREFIX}/${PREFIX}.prm"
echo

VOLUME=$((fcsv2points.py --output-volume-filename ${ARGS} "${TMPDIR}/${PREFIX}/${PREFIX}.points") 2>&1)
echo "volume: ${VOLUME}"
point2model "${TMPDIR}/${PREFIX}/${PREFIX}.points" "${TMPDIR}/${PREFIX}/${PREFIX}.mod"
sitk_convert.py "${VOLUME}" "${TMPDIR}/${PREFIX}/${PREFIX}.mrc"

pushd .
cd "${TMPDIR}/${PREFIX}"
prmParser "${PREFIX}.prm"
processchunks -g "localhost:${N_PROC}" "${PREFIX}"
assemble.sh
popd

cp -r "${TMPDIR}/${PREFIX}" "PEET-${PREFIX}"

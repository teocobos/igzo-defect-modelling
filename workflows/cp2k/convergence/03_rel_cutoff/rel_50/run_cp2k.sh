#!/bin/bash

# ============================================================
# CP2K local execution script
# IGZO Defect Modelling
#
# Usage:
#   ./run_cp2k.sh input.inp
# ============================================================

set -e

export OMP_NUM_THREADS=${OMP_NUM_THREADS:-4}

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input.inp>"
    exit 1
fi

INPUT="$1"

if [ ! -f "$INPUT" ]; then
    echo "ERROR: Input file '$INPUT' not found."
    exit 1
fi

# Remove .inp and generate matching output filename
BASENAME="${INPUT%.inp}"
OUTPUT="${BASENAME}.out"

echo "=========================================="
echo "IGZO CP2K calculation"
echo "=========================================="
echo "Input:        $INPUT"
echo "Output:       $OUTPUT"
echo "OMP threads:  $OMP_NUM_THREADS"
echo "Executable:   $(which cp2k.psmp)"
echo "Start time:   $(date)"
echo "=========================================="

cp2k.psmp -i "$INPUT" -o "$OUTPUT"

EXIT_CODE=$?

echo "=========================================="
echo "End time:     $(date)"
echo "Exit code:    $EXIT_CODE"
echo "=========================================="

exit $EXIT_CODE
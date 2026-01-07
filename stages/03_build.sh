#!/usr/bin/env bash

# Script to build parquet files from EDLists CSV data

set -e

localpath=$(pwd)
echo "Local path: $localpath"

rawpath="$localpath/raw"
echo "Raw path: $rawpath"

# Create brick directory
brickpath="$localpath/brick"
mkdir -p "$brickpath"
echo "Brick path: $brickpath"

# Convert all CSV files to parquet
for csvfile in "$rawpath"/*.csv; do
    if [ -f "$csvfile" ]; then
        filename=$(basename "$csvfile" .csv)
        outfile="$brickpath/${filename}.parquet"
        echo "Converting: $csvfile -> $outfile"
        python3 stages/csv2parquet.py "$csvfile" "$outfile"
    fi
done

echo "Build complete."
echo "Output files:"
ls -la "$brickpath"

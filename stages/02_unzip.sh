#!/usr/bin/env bash

# Script to process EDLists CSV files
# Since we're now downloading CSVs directly (via Wayback Machine HTML parsing),
# this stage just copies them to the raw directory

set -e

localpath=$(pwd)
echo "Local path: $localpath"

downloadpath="$localpath/download"
echo "Download path: $downloadpath"

listpath="$localpath/list"
echo "List path: $listpath"

# Create raw directory
rawpath="$localpath/raw"
mkdir -p "$rawpath"
echo "Raw path: $rawpath"

# Copy CSV files to raw directory
echo "Processing CSV files..."
for csvfile in "$downloadpath"/*.csv; do
    if [ -f "$csvfile" ]; then
        filename=$(basename "$csvfile")
        cp "$csvfile" "$rawpath/$filename"
        echo "  Copied: $filename"
    fi
done

echo ""
echo "Processing complete."
echo "Files in raw/:"
ls -la "$rawpath"

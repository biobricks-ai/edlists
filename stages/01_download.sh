#!/usr/bin/env bash

# Script to download EDLists.org data files
# EDLists.org: EU Endocrine Disruptor Lists
# Source: https://edlists.org/

set -e

localpath=$(pwd)
echo "Local path: $localpath"

# Create directories
listpath="$localpath/list"
mkdir -p "$listpath"
echo "List path: $listpath"

downloadpath="$localpath/download"
mkdir -p "$downloadpath"
echo "Download path: $downloadpath"

# EDLists.org URLs for the three lists
# Note: These pages have "Download XLSX" buttons that generate Excel files

# Create list of expected output files (CSVs from Wayback Machine HTML parsing)
cat > "$listpath/files.txt" << 'EOF'
list_i_eu_identified.csv
list_ii_under_evaluation.csv
list_iii_national_authority.csv
EOF

# Download using Python script (parses HTML tables from Wayback Machine)
# Clever solution: Uses Internet Archive to bypass Cloudflare protection
python3 stages/download_edlists.py "$downloadpath"

echo ""
echo "Download complete."
echo "Note: Data sourced from Internet Archive (February 2024 snapshot)"
ls -la "$downloadpath"

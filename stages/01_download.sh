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

# Create list of source pages
cat > "$listpath/files.txt" << 'EOF'
list_i_eu_identified.xlsx
list_ii_under_evaluation.xlsx
list_iii_national_authority.xlsx
EOF

# Download using Python script (handles JavaScript-rendered content)
python3 stages/download_edlists.py "$downloadpath"

echo "Download complete."
ls -la "$downloadpath"

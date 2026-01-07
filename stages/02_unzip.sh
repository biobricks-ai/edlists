#!/usr/bin/env bash

# Script to process EDLists Excel files to CSV
# Excel files don't need unzipping, but we convert to CSV here

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

# Convert Excel files to CSV using Python
python3 << 'PYEOF'
import pandas as pd
from pathlib import Path

download_path = Path("download")
raw_path = Path("raw")
raw_path.mkdir(exist_ok=True)

xlsx_files = list(download_path.glob("*.xlsx"))
if not xlsx_files:
    print("No Excel files found in download/")
    print("Please download files manually from EDLists.org")
    exit(0)

for xlsx_file in xlsx_files:
    print(f"Converting: {xlsx_file}")
    try:
        # Read all sheets
        xlsx = pd.ExcelFile(xlsx_file)
        for sheet in xlsx.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet)
            # Clean sheet name for filename
            clean_name = sheet.replace(" ", "_").lower()
            output_file = raw_path / f"{xlsx_file.stem}_{clean_name}.csv"
            df.to_csv(output_file, index=False)
            print(f"  -> {output_file} ({len(df)} rows)")
    except Exception as e:
        print(f"  Error: {e}")

print(f"\nConverted files in {raw_path}:")
for f in raw_path.glob("*.csv"):
    print(f"  {f.name}")
PYEOF

echo "Conversion complete."

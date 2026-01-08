#!/usr/bin/env python3
"""
Download EDLists data from Internet Archive (Wayback Machine)
Parses HTML tables from archived pages to extract ED substance lists.

Clever solution: Uses Wayback Machine to bypass Cloudflare protection on edlists.org
"""

import os
import sys
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import csv

# Wayback Machine URLs (February 2024 archive)
LISTS = {
    "list_i_eu_identified": {
        "url": "https://web.archive.org/web/20240203050304/https://edlists.org/the-ed-lists/list-i-substances-identified-as-endocrine-disruptors-by-the-eu",
        "description": "Substances identified as endocrine disruptors at EU level",
    },
    "list_ii_under_evaluation": {
        "url": "https://web.archive.org/web/20240203050308/https://edlists.org/the-ed-lists/list-ii-substances-under-eu-investigation-endocrine-disruption",
        "description": "Substances under EU investigation for endocrine disruption",
    },
    "list_iii_national_authority": {
        "url": "https://web.archive.org/web/20240203050312/https://edlists.org/the-ed-lists/list-iii-substances-identified-as-endocrine-disruptors-by-participating-national-authorities",
        "description": "Substances identified by national authorities as having ED properties",
    },
}


def clean_text(text):
    """Clean whitespace and HTML artifacts from text"""
    if text is None:
        return ""
    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', str(text).strip())
    return text


def parse_edlist_table(url, list_name):
    """Parse HTML table from archived EDLists page"""
    print(f"Fetching: {list_name}")
    print(f"  URL: {url}")

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })

    response = session.get(url, timeout=60)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main data table (EDLists uses cols-7 class)
    table = soup.find('table', class_='cols-7')
    if not table:
        # Try other table patterns
        table = soup.find('table')

    if not table:
        print(f"  WARNING: No table found in {list_name}")
        return [], []

    # Extract headers
    headers = []
    thead = table.find('thead')
    if thead:
        for th in thead.find_all('th'):
            header_text = clean_text(th.get_text())
            # Shorten headers
            header_text = header_text.replace('Name and abbreviation', 'name')
            header_text = header_text.replace('CAS no.', 'cas_number')
            header_text = header_text.replace('EC / List no.', 'ec_list_number')
            header_text = header_text.replace('Health Effects', 'health_effects')
            header_text = header_text.replace('Environmental Effects', 'environmental_effects')
            header_text = header_text.replace('Status', 'status')
            header_text = header_text.replace('Regulatory Field', 'regulatory_field')
            headers.append(header_text)

    # If no headers found in thead, use default
    if not headers:
        headers = ['name', 'cas_number', 'ec_list_number', 'health_effects',
                   'environmental_effects', 'status', 'regulatory_field']

    # Extract rows
    rows = []
    tbody = table.find('tbody') or table
    for tr in tbody.find_all('tr'):
        cells = tr.find_all('td')
        if cells:
            row = [clean_text(td.get_text()) for td in cells]
            if any(row):  # Skip empty rows
                # Pad row to match header length
                while len(row) < len(headers):
                    row.append('')
                rows.append(row[:len(headers)])

    print(f"  Found {len(rows)} substances")
    return headers, rows


def save_csv(headers, rows, output_file):
    """Save data to CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    if len(sys.argv) < 2:
        download_path = Path("download")
    else:
        download_path = Path(sys.argv[1])

    download_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Downloading EDLists from Internet Archive (Wayback Machine)")
    print("Source: edlists.org (February 2024 archive)")
    print("=" * 60)
    print()

    success_count = 0

    for list_name, info in LISTS.items():
        try:
            headers, rows = parse_edlist_table(info["url"], list_name)

            if rows:
                output_file = download_path / f"{list_name}.csv"
                save_csv(headers, rows, output_file)
                print(f"  Saved: {output_file}")
                success_count += 1
            else:
                print(f"  SKIPPED: No data found for {list_name}")

            print()

        except Exception as e:
            print(f"  ERROR processing {list_name}: {e}")
            import traceback
            traceback.print_exc()
            print()

    print("=" * 60)
    if success_count > 0:
        print(f"Download complete! {success_count} lists downloaded.")
    else:
        print("WARNING: No data downloaded. Check network connectivity.")
    print("=" * 60)

    # List downloaded files
    print("\nDownloaded files:")
    for f in download_path.glob("*.csv"):
        size = f.stat().st_size
        print(f"  {f.name}: {size:,} bytes")


if __name__ == "__main__":
    main()

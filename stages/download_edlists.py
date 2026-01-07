#!/usr/bin/env python3
"""
Download EDLists.org Excel files.

EDLists.org provides three lists of endocrine disruptors:
- List I: Substances identified as EDs at EU level
- List II: Substances under evaluation for ED properties
- List III: Substances considered EDs by national authorities

Each list page has a "Download XLSX" button.
"""

import os
import sys
import time
import requests
from pathlib import Path

# EDLists.org list pages
LISTS = {
    "list_i_eu_identified": {
        "url": "https://edlists.org/the-ed-lists/list-i-substances-identified-as-endocrine-disruptors-by-the-eu",
        "description": "Substances identified as endocrine disruptors at EU level",
    },
    "list_ii_under_evaluation": {
        "url": "https://edlists.org/the-ed-lists/list-ii-substances-under-eu-investigation-endocrine-disruption",
        "description": "Substances under evaluation for endocrine disruption under EU legislation",
    },
    "list_iii_national_authority": {
        "url": "https://edlists.org/the-ed-lists/list-iii-substances-identified-as-endocrine-disruptors-by-participating-national-authorities",
        "description": "Substances considered to have ED properties by national authorities",
    },
}


def try_direct_download(download_path: Path) -> bool:
    """
    Try to download Excel files directly from EDLists.org.

    The site may have direct download links or require JavaScript rendering.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })

    success_count = 0

    for list_name, info in LISTS.items():
        print(f"\nProcessing: {list_name}")
        print(f"  URL: {info['url']}")

        try:
            # First, fetch the page to look for download links
            response = session.get(info["url"], timeout=30)
            response.raise_for_status()

            # Look for Excel download link in the page
            # Common patterns: .xlsx links, export endpoints
            html = response.text

            # Try common Excel export patterns
            export_urls = []

            # Pattern 1: Direct .xlsx link
            import re
            xlsx_links = re.findall(r'href="([^"]*\.xlsx[^"]*)"', html, re.IGNORECASE)
            export_urls.extend(xlsx_links)

            # Pattern 2: Export endpoint
            export_links = re.findall(r'href="([^"]*export[^"]*)"', html, re.IGNORECASE)
            export_urls.extend(export_links)

            # Pattern 3: Download button with data attribute
            download_links = re.findall(r'data-href="([^"]*)"', html)
            export_urls.extend(download_links)

            if export_urls:
                for url in export_urls:
                    if not url.startswith("http"):
                        url = f"https://edlists.org{url}" if url.startswith("/") else f"https://edlists.org/{url}"

                    print(f"  Trying: {url}")
                    try:
                        dl_response = session.get(url, timeout=60)
                        if dl_response.status_code == 200 and len(dl_response.content) > 1000:
                            output_file = download_path / f"{list_name}.xlsx"
                            with open(output_file, "wb") as f:
                                f.write(dl_response.content)
                            print(f"  Downloaded: {output_file}")
                            success_count += 1
                            break
                    except Exception as e:
                        print(f"  Failed: {e}")
            else:
                print("  No direct download links found")
                print("  Manual download may be required from the website")

        except Exception as e:
            print(f"  Error: {e}")

        time.sleep(1)  # Be nice to the server

    return success_count > 0


def create_placeholder_instructions(download_path: Path):
    """Create a README with manual download instructions."""
    readme = download_path / "DOWNLOAD_INSTRUCTIONS.md"
    readme.write_text("""# EDLists.org Manual Download Instructions

The EDLists.org website uses JavaScript to generate Excel downloads.
Please manually download the files from:

## List I - EU Identified EDs
URL: https://edlists.org/the-ed-lists/list-i-substances-identified-as-endocrine-disruptors-by-the-eu
- Click "Download XLSX" button at bottom of table
- Save as: list_i_eu_identified.xlsx

## List II - Under EU Evaluation
URL: https://edlists.org/the-ed-lists/list-ii-substances-under-eu-investigation-endocrine-disruption
- Click "Download XLSX" button at bottom of table
- Save as: list_ii_under_evaluation.xlsx

## List III - National Authority Identified
URL: https://edlists.org/the-ed-lists/list-iii-substances-identified-as-endocrine-disruptors-by-participating-national-authorities
- Click "Download XLSX" button at bottom of table
- Save as: list_iii_national_authority.xlsx

Place all downloaded files in this download/ directory.
""")
    print(f"\nCreated: {readme}")


def main():
    if len(sys.argv) < 2:
        print("Usage: download_edlists.py <download_path>")
        sys.exit(1)

    download_path = Path(sys.argv[1])
    download_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("EDLists.org Data Download")
    print("=" * 60)

    # Try automatic download
    success = try_direct_download(download_path)

    if not success:
        print("\n" + "=" * 60)
        print("Automatic download did not succeed.")
        print("Creating manual download instructions...")
        create_placeholder_instructions(download_path)

    print("\nDownload stage complete.")


if __name__ == "__main__":
    main()

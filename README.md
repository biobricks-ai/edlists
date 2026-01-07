# EDLists.org - EU Endocrine Disruptor Lists

A BioBricks.ai brick containing the official EU Endocrine Disruptor Lists from EDLists.org, maintained by national authorities of Belgium, Denmark, France, The Netherlands, Sweden, and Spain.

## Description

EDLists.org provides three authoritative lists of substances identified as endocrine disruptors or under evaluation within the EU regulatory framework.

### The Three Lists

| List | Description |
|------|-------------|
| **List I** | Substances **identified** as endocrine disruptors at EU level (legally adopted under REACH, PPPR, BPR, or Cosmetics Regulation) |
| **List II** | Substances **under evaluation** for endocrine disruption under EU legislation |
| **List III** | Substances **considered** by national authorities to have ED properties |

### Data Columns

Each list contains:
- **Name and abbreviation** - Chemical name
- **CAS number** - Chemical Abstracts Service registry number
- **EC / List no.** - EINECS/ELINCS number
- **Health effects** - Yes/No indicator
- **Environmental effects** - Yes/No indicator
- **Status** - Regulatory status (e.g., "Legally adopted", "Candidate list")
- **Year** - Year of listing
- **Regulatory Field** - REACH, PPPR, BPR, Cosmetics

## Data Contents

| File | Description |
|------|-------------|
| `list_i_eu_identified.parquet` | Substances legally identified as EDs at EU level |
| `list_ii_under_evaluation.parquet` | Substances under EU investigation |
| `list_iii_national_authority.parquet` | Substances identified by national authorities |

## Usage

```python
import biobricks as bb

bb.install("edlists")
edlists = bb.load("edlists")

# Load List I (legally identified EDs)
import pandas as pd
list_i = pd.read_parquet(edlists.brick_path / "list_i_eu_identified.parquet")

# Check regulatory status
print(list_i.columns)
print(f"Total EU-identified EDs: {len(list_i)}")
```

### Check if a compound is regulated

```python
import pandas as pd

# Load all three lists
list_i = pd.read_parquet("brick/list_i_eu_identified.parquet")
list_ii = pd.read_parquet("brick/list_ii_under_evaluation.parquet")
list_iii = pd.read_parquet("brick/list_iii_national_authority.parquet")

# Search by CAS number
cas = "80-05-7"  # Bisphenol A

def find_in_lists(cas_number):
    results = {}
    for name, df in [("List I", list_i), ("List II", list_ii), ("List III", list_iii)]:
        # Handle various CAS column names
        cas_col = [c for c in df.columns if 'cas' in c.lower()][0]
        matches = df[df[cas_col].astype(str).str.contains(cas_number, na=False)]
        if len(matches) > 0:
            results[name] = matches
    return results

matches = find_in_lists(cas)
for list_name, data in matches.items():
    print(f"{list_name}: Found {len(data)} entries")
```

## Source

**EDLists.org**
Website: https://edlists.org/
Maintained by national authorities of Belgium, Denmark, France, The Netherlands, Sweden, and Spain.

### Regulatory Frameworks

- **REACH** - Registration, Evaluation, Authorisation and Restriction of Chemicals
- **PPPR** - Plant Protection Products Regulation
- **BPR** - Biocidal Products Regulation
- **Cosmetics Regulation** - EU Cosmetics Regulation

### Citation

When using this data, please cite EDLists.org:
> EDLists.org. Endocrine Disruptor Lists. https://edlists.org/
> Maintained by national authorities of BE, DK, FR, NL, SE, ES.

## Related Resources

- **DEDuCT** - Database of EDCs with experimental evidence
- **CompTox Dashboard** - EPA chemical safety data
- **ECHA ED Assessment** - European Chemicals Agency ED assessments

## License

Data is provided by EDLists.org under their terms of use for informational purposes.

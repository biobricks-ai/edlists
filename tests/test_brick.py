#!/usr/bin/env python3
"""Tests for EDLists biobrick data integrity."""

import pytest
import pandas as pd
from pathlib import Path

BRICK_DIR = Path(__file__).parent.parent / "brick"

# Expected files and their minimum row counts
EXPECTED_FILES = {
    "list_i_eu_identified.parquet": 100,  # ~109 EU-identified EDs
    "list_ii_under_evaluation.parquet": 50,  # ~71 under evaluation
    "list_iii_national_authority.parquet": 1,  # ~3 national authority
}

# Expected columns based on EDLists.org structure
EXPECTED_COLUMNS = ["name", "cas_number", "ec_list_number", "health_effects",
                    "environmental_effects", "status", "regulatory_field"]


class TestBrickFiles:
    """Test that brick files exist and are valid parquet."""

    def test_brick_directory_exists(self):
        assert BRICK_DIR.exists(), f"Brick directory not found: {BRICK_DIR}"

    @pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
    def test_parquet_file_exists(self, filename):
        filepath = BRICK_DIR / filename
        assert filepath.exists(), f"Expected file not found: {filename}"

    @pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
    def test_parquet_file_readable(self, filename):
        filepath = BRICK_DIR / filename
        df = pd.read_parquet(filepath)
        assert len(df) > 0, f"File {filename} is empty"


class TestDataIntegrity:
    """Test data integrity and expected content."""

    def test_list_i_row_count(self):
        df = pd.read_parquet(BRICK_DIR / "list_i_eu_identified.parquet")
        min_rows = EXPECTED_FILES["list_i_eu_identified.parquet"]
        assert len(df) >= min_rows, f"Expected at least {min_rows} rows, got {len(df)}"

    def test_list_ii_row_count(self):
        df = pd.read_parquet(BRICK_DIR / "list_ii_under_evaluation.parquet")
        min_rows = EXPECTED_FILES["list_ii_under_evaluation.parquet"]
        assert len(df) >= min_rows, f"Expected at least {min_rows} rows, got {len(df)}"

    def test_list_iii_row_count(self):
        df = pd.read_parquet(BRICK_DIR / "list_iii_national_authority.parquet")
        min_rows = EXPECTED_FILES["list_iii_national_authority.parquet"]
        assert len(df) >= min_rows, f"Expected at least {min_rows} rows, got {len(df)}"

    def test_list_i_has_expected_columns(self):
        df = pd.read_parquet(BRICK_DIR / "list_i_eu_identified.parquet")
        cols_lower = [c.lower() for c in df.columns]
        # Check for key columns
        assert any("name" in c for c in cols_lower), "Missing name column"
        assert any("cas" in c for c in cols_lower), "Missing CAS number column"

    def test_no_completely_empty_dataframes(self):
        for filename in EXPECTED_FILES.keys():
            df = pd.read_parquet(BRICK_DIR / filename)
            assert not df.isna().all().all(), f"File {filename} has all null values"


class TestDataQuality:
    """Test data quality metrics."""

    def test_list_i_has_substance_names(self):
        df = pd.read_parquet(BRICK_DIR / "list_i_eu_identified.parquet")
        name_cols = [c for c in df.columns if "name" in c.lower()]
        if name_cols:
            name_col = name_cols[0]
            non_null_ratio = df[name_col].notna().mean()
            assert non_null_ratio > 0.9, f"Too many missing names: {non_null_ratio:.1%}"

    def test_list_i_has_cas_numbers(self):
        df = pd.read_parquet(BRICK_DIR / "list_i_eu_identified.parquet")
        cas_cols = [c for c in df.columns if "cas" in c.lower()]
        if cas_cols:
            cas_col = cas_cols[0]
            # At least 50% should have CAS numbers
            non_null_ratio = df[cas_col].notna().mean()
            assert non_null_ratio > 0.5, f"Too many missing CAS numbers: {non_null_ratio:.1%}"

    def test_combined_substance_count(self):
        """Test total substances across all lists."""
        total = 0
        for filename in EXPECTED_FILES.keys():
            df = pd.read_parquet(BRICK_DIR / filename)
            total += len(df)
        # EDLists should have ~183 substances total
        assert total >= 150, f"Expected at least 150 total substances, got {total}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

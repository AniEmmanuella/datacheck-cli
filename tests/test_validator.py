
"""Tests for the DataCheck CSV validator."""

import csv

import pytest

from datacheck.validator import validate_csv


def test_valid_and_invalid_records(tmp_path):
    """Separate valid records from records with missing values."""
    csv_file = tmp_path / "people.csv"
    csv_file.write_text(
        "name,email,age\n"
        "Ella,ella@example.com,22\n"
        "Mary,,21\n"
        "John,john@example.com,25\n",
        encoding="utf-8",
    )

    result = validate_csv(csv_file)

    assert result.total_rows == 3
    assert result.valid_count == 2
    assert result.invalid_count == 1
    assert result.valid_rows[0]["name"] == "Ella"
    assert result.invalid_rows[0]["record"]["name"] == "Mary"


def test_required_columns(tmp_path):
    """Reject a CSV that lacks a requested column."""
    csv_file = tmp_path / "people.csv"
    csv_file.write_text(
        "name,email\nElla,ella@example.com\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Required columns are missing"):
        validate_csv(csv_file, required_columns=["name", "age"])


def test_missing_input_file(tmp_path):
    """Raise an informative error when the file does not exist."""
    with pytest.raises(FileNotFoundError):
        validate_csv(tmp_path / "missing.csv")


def test_empty_csv_file(tmp_path):
    """Reject an empty CSV file."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="no header"):
        validate_csv(csv_file)


def test_whitespace_only_required_value(tmp_path):
    """Treat whitespace-only required values as invalid."""
    csv_file = tmp_path / "people.csv"
    csv_file.write_text(
        "name,email\n"
        "Ella,ella@example.com\n"
        "John,   \n",
        encoding="utf-8",
    )

    result = validate_csv(csv_file)

    assert result.valid_count == 1
    assert result.invalid_count == 1


def test_duplicate_headers(tmp_path):
    """Reject duplicate column names."""
    csv_file = tmp_path / "duplicate.csv"
    csv_file.write_text(
        "name,name\nElla,Emmanuella\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate column names"):
        validate_csv(csv_file)



"""Validation utilities for CSV datasets."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ValidationResult:
    """Store the results of validating a CSV dataset."""

    valid_rows: list[dict[str, str]]
    invalid_rows: list[dict[str, Any]]
    total_rows: int

    @property
    def valid_count(self) -> int:
        """Return the number of valid rows."""
        return len(self.valid_rows)

    @property
    def invalid_count(self) -> int:
        """Return the number of invalid rows."""
        return len(self.invalid_rows)


def validate_csv(
    input_path: str | Path,
    required_columns: list[str] | None = None,
) -> ValidationResult:
    """Validate a CSV file and separate valid and invalid records.

    A record is invalid if a required column is missing or any
    required field contains an empty or whitespace-only value.

    Args:
        input_path: Path to the input CSV file.
        required_columns: Column names that must exist and be populated.
            If omitted, all columns are treated as required.

    Returns:
        A ValidationResult containing valid and invalid records.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the CSV file has no header or duplicate columns.
        OSError: If the file cannot be read.
    """
    path = Path(input_path)

    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The CSV file is empty or has no header.")

        headers = reader.fieldnames

        if len(headers) != len(set(headers)):
            raise ValueError("The CSV file contains duplicate column names.")

        columns_to_check = required_columns or headers

        missing_columns = [
            column for column in columns_to_check if column not in headers
        ]

        if missing_columns:
            raise ValueError(
                "Required columns are missing: "
                + ", ".join(missing_columns)
            )

        valid_rows: list[dict[str, str]] = []
        invalid_rows: list[dict[str, Any]] = []
        total_rows = 0

        for row_number, row in enumerate(reader, start=2):
            total_rows += 1

            # DictReader stores extra fields under the None key.
            reasons: list[str] = []

            if None in row:
                reasons.append("Record contains more values than the header.")

            if any(value is None for value in row.values()):
                reasons.append("Record contains missing values.")

            for column in columns_to_check:
                value = row.get(column)

                if value is None or not value.strip():
                    reasons.append(f"'{column}' is required.")

            # Preserve the original record and attach its validation errors.
            record = {
                key: value
                for key, value in row.items()
                if key is not None
            }

            if reasons:
                invalid_rows.append(
                    {
                        "row_number": row_number,
                        "record": record,
                        "errors": reasons,
                    }
                )
            else:
                valid_rows.append(record)

    return ValidationResult(
        valid_rows=valid_rows,
        invalid_rows=invalid_rows,
        total_rows=total_rows,
    )


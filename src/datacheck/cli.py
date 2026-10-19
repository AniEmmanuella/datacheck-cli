"""Command-line interface for the DataCheck toolkit."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Sequence

from datacheck.validator import validate_csv


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="datacheck",
        description=(
            "Validate a CSV file and separate valid and invalid records."
        ),
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("clean.csv"),
        help="Destination for valid records (default: clean.csv).",
    )

    parser.add_argument(
        "--invalid-output",
        type=Path,
        default=Path("invalid.csv"),
        help="Destination for invalid records (default: invalid.csv).",
    )

    parser.add_argument(
        "--required",
        nargs="+",
        metavar="COLUMN",
        help="Columns that must exist and contain non-empty values.",
    )

    return parser


def write_clean_csv(
    output_path: Path,
    input_path: Path,
    rows: list[dict[str, str]],
) -> None:
    """Write valid records to a CSV file, preserving input column order."""
    with input_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as source:
        reader = csv.reader(source)
        headers = next(reader, None)

    if not headers:
        raise ValueError("Cannot write output: the input has no CSV header.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w", encoding="utf-8", newline=""
    ) as destination:
        writer = csv.DictWriter(
            destination,
            fieldnames=headers,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_invalid_csv(
    output_path: Path,
    input_path: Path,
    invalid_rows: list[dict[str, object]],
) -> None:
    """Write invalid records with their row numbers and error explanations."""
    with input_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as source:
        reader = csv.reader(source)
        headers = next(reader, None)

    if not headers:
        raise ValueError("Cannot write output: the input has no CSV header.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_headers = ["row_number", *headers, "errors"]

    with output_path.open(
        "w", encoding="utf-8", newline=""
    ) as destination:
        writer = csv.DictWriter(
            destination,
            fieldnames=output_headers,
            extrasaction="ignore",
        )
        writer.writeheader()

        for item in invalid_rows:
            record = item["record"]
            errors = item["errors"]

            if not isinstance(record, dict) or not isinstance(errors, list):
                raise ValueError("Unexpected invalid-record format.")

            output_row: dict[str, object] = {
                "row_number": item["row_number"],
                **record,
                "errors": "; ".join(str(error) for error in errors),
            }
            writer.writerow(output_row)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the DataCheck command-line application."""
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path: Path = args.input
    output_path: Path = args.output
    invalid_output_path: Path = args.invalid_output

    if not input_path.is_file():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 2

    resolved_input = input_path.resolve()
    resolved_outputs = {
        output_path.resolve(),
        invalid_output_path.resolve(),
    }

    if len(resolved_outputs) != 2:
        print(
            "Error: Clean and invalid output paths must be different.",
            file=sys.stderr,
        )
        return 2

    if resolved_input in resolved_outputs:
        print(
            "Error: Output paths must not overwrite the input file.",
            file=sys.stderr,
        )
        return 2

    try:
        result = validate_csv(
            input_path,
            required_columns=args.required,
        )

        write_clean_csv(output_path, input_path, result.valid_rows)

        write_invalid_csv(
            invalid_output_path,
            input_path,
            result.invalid_rows,
        )

    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print("DataCheck validation complete.")
    print(f"Total records:   {result.total_rows}")
    print(f"Valid records:   {result.valid_count}")
    print(f"Invalid records: {result.invalid_count}")
    print(f"Clean output:    {output_path}")
    print(f"Invalid output:  {invalid_output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Tests for the DataCheck command-line interface."""

import csv

from datacheck.cli import main


def test_cli_creates_clean_and_invalid_outputs(tmp_path):
    """Write valid and invalid records to separate output files."""
    input_file = tmp_path / "input.csv"
    clean_file = tmp_path / "clean.csv"
    invalid_file = tmp_path / "invalid.csv"

    input_file.write_text(
        "name,email\n"
        "Ella,ella@example.com\n"
        "Mary,\n"
        "John,john@example.com\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            str(input_file),
            "--output",
            str(clean_file),
            "--invalid-output",
            str(invalid_file),
        ]
    )

    assert exit_code == 0
    assert clean_file.exists()
    assert invalid_file.exists()

    with clean_file.open(encoding="utf-8", newline="") as file:
        clean_rows = list(csv.DictReader(file))

    with invalid_file.open(encoding="utf-8", newline="") as file:
        invalid_rows = list(csv.DictReader(file))

    assert len(clean_rows) == 2
    assert len(invalid_rows) == 1
    assert invalid_rows[0]["name"] == "Mary"
    assert "email" in invalid_rows[0]["errors"]


def test_cli_missing_input_returns_error(tmp_path):
    """Return a non-zero status when the input file is missing."""
    exit_code = main([str(tmp_path / "missing.csv")])

    assert exit_code == 2


def test_cli_prevents_overwriting_input(tmp_path):
    """Refuse to use the input file as an output destination."""
    input_file = tmp_path / "input.csv"
    input_file.write_text(
        "name,email\nElla,ella@example.com\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            str(input_file),
            "--output",
            str(input_file),
            "--invalid-output",
            str(tmp_path / "invalid.csv"),
        ]
    )

    assert exit_code == 2
    assert input_file.read_text(encoding="utf-8").startswith("name,email")


def test_cli_prevents_identical_output_paths(tmp_path):
    """Reject identical clean and invalid output paths."""
    input_file = tmp_path / "input.csv"
    input_file.write_text(
        "name,email\nElla,ella@example.com\n",
        encoding="utf-8",
    )

    output_file = tmp_path / "output.csv"

    exit_code = main(
        [
            str(input_file),
            "--output",
            str(output_file),
            "--invalid-output",
            str(output_file),
        ]
    )

    assert exit_code == 2
    assert not output_file.exists()


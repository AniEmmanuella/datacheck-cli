\# DataCheck CLI Toolkit



A typed Python command-line toolkit for validating CSV datasets, identifying invalid records, and separating clean data from records that require attention.



\## Features



\* Validates CSV files using configurable required columns.

\* Identifies records with missing or empty required values.

\* Separates valid records from invalid records.

\* Records the row number and validation errors for each invalid record.

\* Provides command-line options for specifying input and output files.

\* Prevents output files from overwriting the input file.

\* Includes automated tests for validation logic and CLI behaviour.



\## Project Structure



```text

datacheck-cli/

├── examples/

│   ├── sample.csv

│   ├── clean.csv

│   └── invalid.csv

├── src/

│   └── datacheck/

│       ├── \_\_init\_\_.py

│       ├── cli.py

│       └── validator.py

├── tests/

│   ├── test\_cli.py

│   └── test\_validator.py

├── PERFORMANCE.md

├── pyproject.toml

├── requirements.txt

└── README.md

```



\## Requirements



\* Python 3.10 or later

\* pip

\* pytest for running the automated tests



The application uses Python's standard library for CSV processing.



\## Installation



Clone the repository and navigate to the project directory.



Install the project in editable mode:





python -m pip install -e .





Install the testing dependency:



python -m pip install -r requirements.txt





\## Usage



Run the toolkit against a CSV file:





datacheck examples/sample.csv





By default, the application writes valid records to `clean.csv` and invalid records to `invalid.csv` in the current working directory.



Specify output paths:





datacheck examples/sample.csv --output examples/clean.csv --invalid-output examples/invalid.csv





Specify required columns:





datacheck examples/sample.csv --output examples/clean.csv --invalid-output examples/invalid.csv --required name email age





The required columns must exist in the CSV header and contain non-empty values in every valid record.



\## Output Files



\### Clean output



The clean output contains records that pass validation. It preserves the original CSV column order.



\### Invalid output



The invalid output contains records that fail validation, together with their original row numbers and explanations of the validation errors.



\## Example Results



Running the toolkit against the included six-record sample dataset produced:



\* Total records: 6

\* Valid records: 3

\* Invalid records: 3



These figures describe the included sample dataset, not a general performance benchmark.



\## Running the Tests



Run the automated test suite from the project root:





python -m pytest -v





The tests cover valid and invalid records, missing required columns, missing input files, empty CSV files, duplicate headers, whitespace-only values, and CLI output behaviour.



\## Error Handling



The toolkit reports errors for missing input files, CSV files without headers, duplicate column names, missing required columns, and conflicting output paths.



A successful run returns exit code `0`. Input or validation errors handled by the CLI return exit code `2`.



\## Performance



See \[PERFORMANCE.md](PERFORMANCE.md) for the initial test result and guidance on measuring runtime and memory usage.



\## Limitations



\* The toolkit currently supports CSV input.

\* Required-field validation checks for empty or whitespace-only values; it does not validate email formats, numeric ranges, or other domain-specific rules.

\* The current implementation processes records in memory, so memory consumption increases with dataset size.

\* The performance of larger datasets has not yet been benchmarked.



\## Author



Developed as part of the Week 3 project: Typed CLI Toolkit.




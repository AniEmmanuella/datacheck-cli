\# DataCheck CLI Toolkit — Performance Report



\## 1. Overview



DataCheck is a typed Python command-line toolkit for validating CSV datasets, identifying invalid records, and separating valid records from records that require attention.



This report documents the automated test results, functional execution, and an initial benchmark using 100,000 CSV records.



\## 2. Automated Test Results



The automated test suite was executed using:



`python -m pytest -v`



Results:



\* Tests passed: 10

\* Tests failed: 0

\* Reported test-suite duration: 0.17 seconds



The test-suite duration measures the automated tests and is separate from the CLI benchmark.



\## 3. Sample Dataset Results



The toolkit was tested against the included six-record sample dataset.



| Metric          | Result |

| --------------- | -----: |

| Total records   |      6 |

| Valid records   |      3 |

| Invalid records |      3 |



The clean and invalid output files were generated successfully.



\## 4. Large-Dataset Benchmark



\### Test setup



A generated CSV dataset containing 100,000 records was processed using the DataCheck CLI.



The command used was:



`Measure-Command { datacheck .\\examples\\benchmark.csv --output .\\examples\\benchmark\_clean.csv --invalid-output .\\examples\\benchmark\_invalid.csv --required name email age }`



\### Results



| Metric                   |          Result |

| ------------------------ | --------------: |

| Input records            |         100,000 |

| Valid records            |         100,000 |

| Invalid records          |               0 |

| Total execution time     |   1.055 seconds |

| Input file size          | 3,977,796 bytes |

| Clean output file size   | 3,977,796 bytes |

| Invalid output file size |        34 bytes |



All generated records passed validation. The invalid output file contained its header but no invalid data records.



The measured execution time includes reading the input file, validating records, and writing both output files.



This is an initial benchmark from one loc




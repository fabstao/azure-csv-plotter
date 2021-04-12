# Plotter for CSV Azure collector

This app plots data from CSVs retrieved from:
[https://github.com/fabstao/azure-ps-storage-metrics](Azure Storage Metrics)

## Dependencies

Install with pip using requirements.txt:

```
pip install -r requirements.txt
```

## Usage:

Use Pandas to retrieve data from Azure Monitor CSV

Arguments:
  data -- Pandas DataFrame
  nombre -- filename with full path

Return value:
  Null

This function will output PDF files with plot from CSVs

Usage:

```
python3 analyze.py <path>
python3 tsummary.py <path>
```

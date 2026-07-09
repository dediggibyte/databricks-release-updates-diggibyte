On this page

Last updated on **Jun 12, 2026**

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). Workspace admins can control access to this feature from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

Databricks includes built-in support for reading `.xls` and `.xlsx` files, eliminating the need for external libraries or manual file conversions. You can read any sheet from a multi-sheet workbook, target specific cell ranges, automatically infer schema and data types, and work with formula values as their computed results. Excel files can be read from cloud storage or uploaded directly in the **Add Data** UI, and support both batch and streaming workloads using Auto Loader.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Reading and streaming Excel files requires Databricks Runtime 17.1 or above and [Auto Loader](/aws/en/ingestion/cloud-object-storage/auto-loader/) for streaming workloads.

## Options[​](#options "Direct link to Options")

Use the `.option()` and `.options()` methods of `DataFrameReader` to configure Excel data sources. For a complete list of supported options, see [`DataFrameReader` Excel options](/aws/en/spark/api-options#batch-reader-excel) and [`DataFrameWriter` Excel options](/aws/en/spark/api-options#batch-writer-excel).

## Usage[​](#usage "Direct link to Usage")

The following examples demonstrate reading Excel files using the Spark batch (`spark.read`) and streaming APIs. By default, the parser reads all cells from the top-left to the bottom-right non-empty cell in the first sheet; use the `dataAddress` option to target a specific sheet or cell range. Schema is inferred automatically, or you can specify your own.

### Create or modify a table in the UI[​](#create-or-modify-a-table-in-the-ui "Direct link to Create or modify a table in the UI")

You can use the **Create or modify table** UI to create tables from Excel files. Start by [uploading an Excel file](/aws/en/ingestion/create-or-modify-table) or [selecting an Excel file from a volume or an external location](/aws/en/ingestion/cloud-object-storage/add-data-external-locations). Choose the sheet, adjust the number of header rows, and optionally specify a cell range. The UI supports creating a single table from the selected file and sheet.

### Read Excel files[​](#read-excel-files "Direct link to Read Excel files")

You can read an Excel file from cloud storage (for example, S3, ADLS) using `spark.read.excel` or SQL's `read_files` function.

* Python
* SQL

Python

```
# Read the first sheet from a single Excel file or from multiple Excel files in a directory  
df = (spark.read.excel(<path to excel directory or file>))  
  
# Infer schema field name from the header row  
df = (spark.read  
       .option("headerRows", 1)  
       .excel(<path to excel directory or file>))  
  
# Read a specific sheet and range  
df = (spark.read  
       .option("headerRows", 1)  
       .option("dataAddress", "Sheet1!A1:E10")  
       .excel(<path to excel directory or file>))
```

SQL

```
-- Read an entire Excel file  
CREATE TABLE my_table AS  
SELECT * FROM read_files(  
  "<path to excel directory or file>",  
  schemaEvolutionMode => "none"  
);  
  
-- Read a specific sheet and range  
CREATE TABLE my_sheet_table AS  
SELECT * FROM read_files(  
  "<path to excel directory or file>",  
  format => "excel",  
  headerRows => 1,  
  dataAddress => "Sheet1!A2:D10",  
  schemaEvolutionMode => "none"  
);
```

### Stream Excel files using Auto Loader[​](#stream-excel-files-using-auto-loader "Direct link to stream-excel-files-using-auto-loader")

You can stream Excel files using Auto Loader by setting `cloudFiles.format` to `excel`. For example:

Python

```
df = (  
  spark  
    .readStream  
    .format("cloudFiles")  
    .option("cloudFiles.format", "excel")  
    .option("cloudFiles.inferColumnTypes", True)  
    .option("headerRows", 1)  
    .option("cloudFiles.schemaLocation", "<path to schema location dir>")  
    .option("cloudFiles.schemaEvolutionMode", "none")  
    .load(<path to excel directory or file>)  
)  
df.writeStream  
  .format("delta")  
  .option("mergeSchema", "true")  
  .option("checkpointLocation", "<path to checkpoint location dir>")  
  .table(<table name>)
```

### Ingest Excel files using `COPY INTO`[​](#ingest-excel-files-using-copy-into "Direct link to ingest-excel-files-using-copy-into")

Use `COPY INTO` to load Excel files from cloud storage into a Delta table idempotently.

SQL

```
CREATE TABLE IF NOT EXISTS excel_demo_table;  
  
COPY INTO excel_demo_table  
FROM "<path to excel directory or file>"  
FILEFORMAT = EXCEL  
FORMAT_OPTIONS ('mergeSchema' = 'true')  
COPY_OPTIONS ('mergeSchema' = 'true');
```

### List sheets[​](#list-sheets "Direct link to List sheets")

You can list the sheets in an Excel file using the `listSheets` operation. The returned schema is a `struct` with the following fields:

* `sheetIndex`: long
* `sheetName`: String

For example:

* Python
* SQL

Python

```
# List the name of the Sheets in an Excel file  
df = (spark.read.format("excel")  
       .option("operation", "listSheets")  
       .load(<path to excel directory or file>))
```

SQL

```
SELECT * FROM read_files("<path to excel directory or file>",  
  schemaEvolutionMode => "none",  
  operation => "listSheets"  
)
```

### Parse complex non-structured Excel sheets[​](#parse-complex-non-structured-excel-sheets "Direct link to Parse complex non-structured Excel sheets")

For complex, non-structured Excel sheets (for example, multiple tables per sheet, data islands), Databricks recommends extracting the cell ranges you need to create your Spark DataFrames using the `dataAddress` options.

Python

```
df = (spark.read.format("excel")  
       .option("headerRows", 1)  
       .option("dataAddress", "Sheet1!A1:E10")  
       .load(<path to excel directory or file>))
```

## Limitations[​](#limitations "Direct link to Limitations")

* Password-protected files are not supported.
* Only one header row is supported.
* Merged cell values only populate the top-left cell. Remaining child cells are set to `NULL`.
* Streaming Excel files using Auto Loader is supported, but schema evolution is not. You must explicitly set `schemaEvolutionMode="None"`.
* "Strict Open XML Spreadsheet (Strict OOXML)" is not supported.
* Macro execution in `.xlsm` files is not supported.
* The `ignoreCorruptFiles` option is not supported.

## FAQ[​](#faq "Direct link to FAQ")

Find answers to frequently asked questions about the Excel connector in Lakeflow Connect.

**Can I read all sheets at once?**

The parser reads only one sheet from an Excel file at a time. By default, it reads the first sheet. You can specify a different sheet using the `dataAddress` option. To process multiple sheets, first retrieve the list of sheets by setting the `operation` option to `listSheets`, then iterate over the sheet names and read each one by providing its name in the `dataAddress` option.

**Can I ingest Excel files with complex layouts or multiple tables per sheet?**

By default, the parser reads all Excel cells from the top-left cell to the bottom-right non-empty cell. You can specify a different cell range using the `dataAddress` option.

**How are formulas and merged cells handled?**

Formulas are ingested as their computed values. For merged cells, only the top-left value is retained (child cells are `NULL`).

**Can I use Excel ingestion in Auto Loader and streaming jobs?**

Yes, you can stream Excel files using `cloudFiles.format = "excel"`. However, schema evolution is not supported, so you must set `"schemaEvolutionMode"` to `"None"`.

**Is password-protected Excel supported?**

No. If this functionality is critical to your workflows, contact your Databricks account representative.

## Additional resources[​](#additional-resources "Direct link to Additional resources")

* [Read and write CSV files](/aws/en/query/formats/csv): If your data source can export to CSV, CSV is a simpler format with broader tooling support and no dependency on a dedicated parser.
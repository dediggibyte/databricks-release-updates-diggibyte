AI/BI dashboards have limits on pages, datasets, widgets, filter values, rendered rows, subscription attachments, and PDF downloads. Dataset size has no hard limit, but large datasets are processed differently.

## Dashboard structure limits

The following limits apply to the overall structure and components of AI/BI dashboards:

| Limit | Maximum value | Description |
| --- | --- | --- |
| **Pages per dashboard** | 15 pages | A canvas can contain up to fifteen pages. New dashboards start with a single page. |
| **Datasets per dashboard** | 100 datasets | Define up to 100 datasets per dashboard. Datasets can be created from SQL queries, Unity Catalog tables or views, or uploaded files. |
| **Widgets per dashboard** | 100 widgets per page | Dashboards can hold up to 100 widgets per page. Widgets include visualizations, filters, text boxes, and images. |

←✕

| Limit | Maximum value | Description |
| --- | --- | --- |
| **Pages per dashboard** | 15 pages | A canvas can contain up to fifteen pages. New dashboards start with a single page. |
| **Datasets per dashboard** | 100 datasets | Define up to 100 datasets per dashboard. Datasets can be created from SQL queries, Unity Catalog tables or views, or uploaded files. |
| **Widgets per dashboard** | 100 widgets per page | Dashboards can hold up to 100 widgets per page. Widgets include visualizations, filters, text boxes, and images. |

## Filter limits

The following limits apply to filters and parameter value lists on AI/BI dashboards:

| Limit | Maximum value | Description |
| --- | --- | --- |
| **Dropdown and multiselect filter values** | 100,000 values | Dropdown and multiselect filters can render up to 100,000 distinct values. If the dataset contains more than 100,000 values, any values beyond that limit won’t appear in the list but users can still enter them manually. However, the search doesn't return matches for values that exceed the 100,000-value rendering limit. |
| **Pasted values in multiselect filters** | 1,000 values | When pasting into a multiselect dropdown filter, up to 1,000 values are accepted per paste. Values beyond this limit are dropped. Pasted values can be separated by tabs, newlines, or commas, such as when copying from Excel or Google Sheets. |
| **Values in a parameter value list** | 50 values | A value list on a dashboard parameter can hold up to 50 values. See [Add a value list to a parameter](/aws/en/dashboards/manage/filters/parameters#value-lists). |

←✕

| Limit | Maximum value | Description |
| --- | --- | --- |
| **Dropdown and multiselect filter values** | 100,000 values | Dropdown and multiselect filters can render up to 100,000 distinct values. If the dataset contains more than 100,000 values, any values beyond that limit won’t appear in the list but users can still enter them manually. However, the search doesn't return matches for values that exceed the 100,000-value rendering limit. |
| **Pasted values in multiselect filters** | 1,000 values | When pasting into a multiselect dropdown filter, up to 1,000 values are accepted per paste. Values beyond this limit are dropped. Pasted values can be separated by tabs, newlines, or commas, such as when copying from Excel or Google Sheets. |
| **Values in a parameter value list** | 50 values | A value list on a dashboard parameter can hold up to 50 values. See [Add a value list to a parameter](/aws/en/dashboards/manage/filters/parameters#value-lists). |

## Visualization rendering limits

The following limits apply to how much data can be rendered in dashboard visualizations:

| Visualization type | Maximum rows | Notes |
| --- | --- | --- |
| **Most visualizations** | 15,000 rows | To optimize performance, most charts can only render 15K rows on the canvas. Otherwise, visualizations can be truncated. This applies to area, bar, line, scatter, pie, heatmap, and other chart visualizations. |
| **Table visualizations** | 100,000 rows | Tables can display up to 100K rows before truncation. |

←✕

| Visualization type | Maximum rows | Notes |
| --- | --- | --- |
| **Most visualizations** | 15,000 rows | To optimize performance, most charts can only render 15K rows on the canvas. Otherwise, visualizations can be truncated. This applies to area, bar, line, scatter, pie, heatmap, and other chart visualizations. |
| **Table visualizations** | 100,000 rows | Tables can display up to 100K rows before truncation. |

note

These row limits apply to the rendering of visualizations on the canvas. For information about dataset size thresholds and performance optimizations, see [Dataset performance thresholds](#dataset-limits).

## Dataset performance thresholds

While there's no hard limit on dataset size, Databricks applies different performance optimizations based on dataset result size:

| Dataset size | Optimization behavior |
| --- | --- |
| **Small datasets** (≤ 100,000 rows or ≤ 100MB) | The dataset result is pulled to the client, and visualization-specific filtering and aggregation are performed in the browser. Only the dataset query appears in the query history. |
| **Large datasets** (> 100,000 rows or > 100MB) | The dataset query text is wrapped in a SQL `WITH` clause, and visualization-specific filtering and aggregation is performed in a query on the backend. The visualization query appears in the query history. |

←✕

| Dataset size | Optimization behavior |
| --- | --- |
| **Small datasets** (≤ 100,000 rows or ≤ 100MB) | The dataset result is pulled to the client, and visualization-specific filtering and aggregation are performed in the browser. Only the dataset query appears in the query history. |
| **Large datasets** (> 100,000 rows or > 100MB) | The dataset query text is wrapped in a SQL `WITH` clause, and visualization-specific filtering and aggregation is performed in a query on the backend. The visualization query appears in the query history. |

For optimal dashboard performance, keep your datasets small by using explicit column selection, `WHERE` clauses, and parameters to scope your SQL queries. See [Dataset optimization and caching](/aws/en/dashboards/caching).

## Dashboard subscription limits

Dashboard subscription emails enforce a 24 MB combined attachment size limit that applies across all attached files. The following table describes individual limits.

| File type | Limit | Behavior when limit exceeded |
| --- | --- | --- |
| **All email attachments combined** (PDF, PNG snapshot, CSV, TSV, and Excel) | 24 MB combined | See below for specific behaviors based on which files exceed the limit. |
| **Excel attachments** | 100,000 rows | Rows beyond 100,000 are not included in the attachment. |

←✕

| File type | Limit | Behavior when limit exceeded |
| --- | --- | --- |
| **All email attachments combined** (PDF, PNG snapshot, CSV, TSV, and Excel) | 24 MB combined | See below for specific behaviors based on which files exceed the limit. |
| **Excel attachments** | 100,000 rows | Rows beyond 100,000 are not included in the attachment. |

### Subscription size limit behavior

The following describes the expected behavior when the combined file size exceeds the 24 MB limit:

* **If the PDF file is greater than 24 MB**: The subscription email doesn't include the PDF attachment or any images. It includes a note that says the dashboard has exceeded the size limit and shows the actual file size of the current dashboard.
* **If the combined file size is greater than 24 MB**: Only the PDF is attached to the email. The inline message includes a link to the dashboard but no image.
* **If tabular attachments are dropped due to the size limit**: The email body includes the following message: "Attachments exceeded the 24 MB email limit and were excluded. Open the dashboard to download full results."

See [Manage scheduled dashboard updates and subscriptions](/aws/en/dashboards/share/schedule-subscribe).

## PDF download limits

These limits apply when you download a published dashboard as a PDF:

| Limit | Maximum value | Behavior when limit exceeded |
| --- | --- | --- |
| **PDF file size** | 50 MB | If the selected pages together exceed 50 MB, the PDF includes only the first selected page, and a warning says "Only the first page was included". If the first selected page alone exceeds 50 MB, the download fails and "Could not generate PDF" appears. |
| **Generation time** | 30 minutes | The download fails and "Could not generate PDF" appears. |

←✕

| Limit | Maximum value | Behavior when limit exceeded |
| --- | --- | --- |
| **PDF file size** | 50 MB | If the selected pages together exceed 50 MB, the PDF includes only the first selected page, and a warning says "Only the first page was included". If the first selected page alone exceeds 50 MB, the download fails and "Could not generate PDF" appears. |
| **Generation time** | 30 minutes | The download fails and "Could not generate PDF" appears. |

See [Download a published dashboard as a PDF](/aws/en/dashboards/share/share#download-pdf).
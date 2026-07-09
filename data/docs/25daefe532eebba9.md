On this page

Last updated on **Jul 7, 2026**

Parameters let you pass values into a metric view when you query it. Use parameters to reuse a single [metric view](/aws/en/business-semantics/metric-views/) definition across different inputs, such as a discount rate or a date window. Reference a parameter anywhere a constant SQL expression is valid, such as in filters, field and measure expressions, the source, and joins. Pass a value as an argument when you query the view.

Parameters reduce duplication. Instead of maintaining a separate metric view for each variant, you define the logic once and let each caller supply its own values. A parameter can include a default value, so callers that don't pass an argument fall back to the default.

note

Materialization isn't currently supported for metric views that define parameters.

## Requirements[​](#requirements "Direct link to Requirements")

Querying a metric view that defines parameters requires a compute resource that meets the minimum version requirements. See [Metric view feature availability](/aws/en/business-semantics/metric-views/feature-availability) for minimum compute version requirements.

## Define parameters[​](#define-parameters "Direct link to define-parameters")

You can define parameters in the Catalog Explorer low-code editor or directly in YAML. After you create a parameter, reference it by name anywhere a constant SQL expression is valid, such as in filters, field and measure expressions, the source, and joins.

To add a parameter in the low-code editor:

1. In the editor heading, click **Add parameter**.
2. Enter a parameter name, for example `start_date` or `offset_int`.
3. Enter a default value and data type.
4. Click **Save**.

The parameter appears in the editor heading after you create it.

To define parameters in YAML, add a top-level `parameters` block to the metric view definition. For the complete field reference and a YAML example, see [Parameters](/aws/en/business-semantics/metric-views/yaml-reference#parameters).

## Query a metric view with parameters[​](#query-a-metric-view-with-parameters "Direct link to query-a-metric-view-with-parameters")

To query a metric view that defines parameters, call the metric view as a table-valued function and pass parameters as arguments. You can pass arguments by name or by position, or omit them to use the default values.

### Pass arguments by name[​](#pass-arguments-by-name "Direct link to pass-arguments-by-name")

To pass an argument by name, use the `=>` operator. The following example passes a `discount` value of `0.15`:

SQL

```
SELECT product, MEASURE(discountedSales)  
FROM catalog.schema.metric_view(discount => 0.15)  
GROUP BY product;
```

### Pass arguments by position[​](#pass-arguments-by-position "Direct link to pass-arguments-by-position")

To pass arguments by position, list the values in the order the parameters are defined. The following example passes the same `discount` value of `0.15`:

SQL

```
SELECT product, MEASURE(discountedSales)  
FROM catalog.schema.metric_view(0.15)  
GROUP BY product;
```

### Use default parameter values[​](#use-default-parameter-values "Direct link to use-default-parameter-values")

To use the default parameter values when you call the metric view, omit arguments. The following queries are equivalent and use all default values:

SQL

```
SELECT product, MEASURE(discountedSales) FROM catalog.schema.metric_view() GROUP BY product;  
SELECT product, MEASURE(discountedSales) FROM catalog.schema.metric_view GROUP BY product;
```

### View the parameters a metric view defines[​](#view-the-parameters-a-metric-view-defines "Direct link to view-the-parameters-a-metric-view-defines")

To see the parameters that a metric view defines, view its YAML definition, which includes the `parameters` block. See [View metric view definition and metadata](/aws/en/business-semantics/metric-views/query#view-details-query).

## Additional resources[​](#-additional-resources "Direct link to -additional-resources")

* [Create a metric view](/aws/en/business-semantics/metric-views/create)
* [Query metric views](/aws/en/business-semantics/metric-views/query)
* [Parameters](/aws/en/business-semantics/metric-views/yaml-reference#parameters)
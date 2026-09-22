**Applies to:**  Databricks SQL  Databricks Runtime

Invokes a function that returns a relation or a set of rows as a [table-reference](/aws/en/sql/language-manual/sql-ref-syntax-qry-select-table-reference).

A TVF can be a:

* SQL user-defined table function.
* The [range](/aws/en/sql/language-manual/functions/range) table-valued function.
* Any table-valued generator function, such as [explode](/aws/en/sql/language-manual/functions/explode).

  **Applies to:**  Databricks SQL  Databricks Runtime 12.2 LTS and above.
* A parameterized [metric view](/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-view).

  **Applies to:**  Databricks SQL  Databricks Runtime 18.2 and above.

  Preview

  This feature is in [Public Preview](/aws/en/release-notes/release-types).

note

[Hive UDTF](/aws/en/sql/language-manual/sql-ref-functions-udf-hive) cannot be invoked as a table-reference, but must be invoked from the `SELECT` or using the [LATERAL VIEW clause](/aws/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view).

## Syntax

SQL

```
function_name ( [ expression [, ...] ] ) [ table_alias ]
```

## Parameters

* **[function\_name](/aws/en/sql/language-manual/sql-ref-names#function-name)**

  A table-valued function. If the function cannot be resolved as a table-valued function, Databricks raises [UNRESOLVABLE\_TABLE\_VALUED\_FUNCTION](/aws/en/error-messages/error-classes#unresolvable_table_valued_function).
* **[expression](/aws/en/sql/language-manual/sql-ref-expression)**

  A combination of one or more values, operators, and SQL functions that results in a value.
* **[table\_alias](/aws/en/sql/language-manual/sql-ref-names#table-alias)**

  An optional label to reference the function result and its columns.

## Common error conditions

* [NUM\_TABLE\_VALUE\_ALIASES\_MISMATCH](/aws/en/error-messages/error-classes#num_table_value_aliases_mismatch)
* [UNRESOLVABLE\_TABLE\_VALUED\_FUNCTION](/aws/en/error-messages/error-classes#unresolvable_table_valued_function)
* [WRONG\_NUM\_ARGS.WITHOUT\_SUGGESTION](/aws/en/error-messages/error-classes#wrong_num_args)

## Examples

SQL

```
-- range call with end  
> SELECT * FROM range(6 + cos(3));  
   0  
   1  
   2  
   3  
   4  
  
-- range call with start and end  
> SELECT * FROM range(5, 10);  
   5  
   6  
   7  
   8  
   9  
  
-- range call with numPartitions  
> SELECT * FROM range(0, 10, 2, 200);  
   0  
   2  
   4  
   6  
   8  
  
-- range call with a table alias  
> SELECT * FROM range(5, 8) AS test;  
   5  
   6  
   7  
  
-- Create a SQL UDTF and invoke it  
> CREATE OR REPLACE FUNCTION table_func(a INT) RETURNS TABLE  
    RETURN SELECT a * c1 AS res FROM VALUES(1), (2), (3), (4) AS T(c1)  
  
> SELECT * FROM table_func(5);  
   5  
  10  
  15  
  20  
  
-- Using lateral correlation  
>  SELECT table_func.res FROM VALUES(10), (20) AS S(c1), LATERAL table_func(c1);  
  10  
  20  
  20  
  40  
  30  
  60  
  40  
  80  
  
-- Scalar functions are not allowed in the FROM clause  
> SELECT * FROM trim('hello  ');  
  Error: UNRESOLVABLE_TABLE_VALUED_FUNCTION
```

On Databricks SQL and Databricks Runtime 12.2 LTS and above:

SQL

```
> SELECT * FROM explode(array(10, 20));  
  10  
  20  
  
> SELECT * FROM inline(array(struct(1, 'a'), struct(2, 'b')));  
 col1 col2  
 ---- ----  
    1    a  
    2    b  
  
> SELECT * FROM posexplode(array(10,20));  
 pos col  
 --- ---  
   0  10  
   1  20  
  
> SELECT * FROM stack(2, 1, 2, 3);  
 col0 col1  
 ---- ----  
    1    2  
    3 null  
  
> SELECT * FROM json_tuple('{"a":1, "b":2}', 'a', 'b');  
  c0  c1  
 --- ---  
   1   2  
  
> SELECT * FROM parse_url('http://spark.apache.org/path?query=1', 'HOST');  
  spark.apache.org  
  
> SELECT * FROM VALUES(1), (2) AS t1(c1), LATERAL explode (ARRAY(3,4)) AS t2(c2);  
 c1 c2  
 -- --  
  1  3  
  1  4  
  2  3  
  2  4
```

On Databricks SQL and Databricks Runtime 18.2 and above, you can invoke a parameterized metric view as a table-valued function. Pass each parameter as a named argument, or omit the arguments to use the defaults when every parameter has one. For a metric view named `discounted_sales_metrics` that defines a `discount` parameter:

SQL

```
-- Pass a named argument  
> SELECT order_priority, measure(discounted_revenue)  
  FROM discounted_sales_metrics(discount => 0.15)  
  GROUP BY ALL;  
  
-- Omit the arguments to use the parameter defaults  
> SELECT order_priority, measure(discounted_revenue)  
  FROM discounted_sales_metrics  
  GROUP BY ALL;
```

## Related articles

* [SELECT](/aws/en/sql/language-manual/sql-ref-syntax-qry-select)
This article explains how Genie usage appears in the Databricks billing system tables, how to query and analyze your Genie costs, and how promotional pricing is reflected in your usage data. It also covers how to understand consumption of the free allowance that Genie provides: each user, excluding service principals, receives 150 DBUs per month free.

note

Until July 31, 2026, Genie One and Genie Agents usage is free. Genie Code remains billed beyond the per-user, per-month 150 DBU free allowance.

For information on setting budgets and cost controls for Genie, see [Manage budgets and cost controls for Genie](/aws/en/genie/budgets).

## Query Genie usage from system tables

To analyze Genie usage and cost, query the `system.billing.usage` table and join it with `system.billing.list_prices`. The `system.billing.usage` table updates every few hours and contains a row for each usage record.

The following columns are most relevant for understanding Genie cost:

| Column | Description |
| --- | --- |
| `billing_origin_product` | Set to `GENIE` for all Genie usage. |
| `sku_name` | The billing SKU. Varies by whether usage is free or billed. See [How Genie usage maps to SKUs](#how-genie-usage-maps-to-skus). |
| `usage_quantity` | The number of DBUs consumed. |
| `usage_metadata.genie.surface` | Identifies which Genie product generated the usage (`GENIE_CODE`, `GENIE_ONE`, or `GENIE_AGENTS`). |
| `usage_metadata.genie.channel` | The access channel, for example `UI`. |
| `identity_metadata.run_as` | The user whose identity was used to run the query. |
| `product_features.genie.offering_type` | The offering type, for example `PAYGO`. |
| `custom_tags` | Includes `{"databricks-product": "genie"}` for Genie usage. |

←✕

| Column | Description |
| --- | --- |
| `billing_origin_product` | Set to `GENIE` for all Genie usage. |
| `sku_name` | The billing SKU. Varies by whether usage is free or billed. See [How Genie usage maps to SKUs](#how-genie-usage-maps-to-skus). |
| `usage_quantity` | The number of DBUs consumed. |
| `usage_metadata.genie.surface` | Identifies which Genie product generated the usage (`GENIE_CODE`, `GENIE_ONE`, or `GENIE_AGENTS`). |
| `usage_metadata.genie.channel` | The access channel, for example `UI`. |
| `identity_metadata.run_as` | The user whose identity was used to run the query. |
| `product_features.genie.offering_type` | The offering type, for example `PAYGO`. |
| `custom_tags` | Includes `{"databricks-product": "genie"}` for Genie usage. |

## How Genie usage maps to SKUs

Genie usage is split across two SKUs based on whether the usage is free or billed, not based on the Genie product.

| SKU | What it contains | Billed? | Listed in `list_prices`? |
| --- | --- | --- | --- |
| Serverless Real-Time Inference (for example, `ENTERPRISE_SERVERLESS_REAL_TIME_INFERENCE_<REGION>`) | All billed Genie usage | Yes | Yes |
| `GENIE_FREE_USAGE` | All free Genie usage. See [promotional pricing](#understand-promotional-pricing-for-genie) for what is free. | No | No |

←✕

| SKU | What it contains | Billed? | Listed in `list_prices`? |
| --- | --- | --- | --- |
| Serverless Real-Time Inference (for example, `ENTERPRISE_SERVERLESS_REAL_TIME_INFERENCE_<REGION>`) | All billed Genie usage | Yes | Yes |
| `GENIE_FREE_USAGE` | All free Genie usage. See [promotional pricing](#understand-promotional-pricing-for-genie) for what is free. | No | No |

Use `usage_metadata.genie.surface` to identify which product generated the usage: `GENIE_CODE`, `GENIE_ONE`, or `GENIE_AGENTS`.

### Billed usage: Serverless Real-Time Inference SKU

Genie usage that exceeds the free usage allowance is billed under the **Serverless Real-Time Inference** SKU. The exact SKU name includes your cloud and region, for example `ENTERPRISE_SERVERLESS_REAL_TIME_INFERENCE_US_WEST_OREGON` on AWS. This SKU is available on all clouds.

Because the Serverless Real-Time Inference SKU is shared with other product lines, always filter by `billing_origin_product = 'GENIE'` to isolate Genie usage.

### Free usage: GENIE\_FREE\_USAGE SKU

note

The `GENIE_FREE_USAGE` SKU only starts appearing on July 20, 2026. Free usage consumed before this date is not visible in the system tables.

All free Genie usage appears under `sku_name = 'GENIE_FREE_USAGE'`. This includes:

* **Usage under the free allowance**: Each user, excluding service principals, has a free monthly allowance of 150 DBUs, which resets on the first of each month.
* Until July 31, 2026, all Genie One and Genie Agents usage is free, captured under the `GENIE_FREE_USAGE` SKU.

This is a free usage SKU. It tracks consumption but does not carry a list price, so it has no corresponding entry in `system.billing.list_prices`. When you join `system.billing.usage` with `system.billing.list_prices`, rows with this SKU return no match. This is expected, because the usage is free.

To distinguish between products within the free usage SKU, filter on `usage_metadata.genie.surface`:

* `GENIE_CODE`: Genie Code free usage
* `GENIE_ONE`: Genie One
* `GENIE_AGENTS`: Genie Agents

## Query Genie usage

### Query billed Genie usage and cost

The following query returns all billed Genie usage, per user and per day. This includes Genie Code and any other Genie usage metered under a priced SKU. It excludes rows under the free usage SKU (`GENIE_FREE_USAGE`).

SQL

```
SELECT  
  u.account_id,  
  u.workspace_id,  
  u.usage_date,  
  u.identity_metadata.run_as AS run_as_user,  
  u.usage_metadata.genie.surface AS genie_surface,  
  u.usage_metadata.genie.channel AS genie_channel,  
  u.sku_name,  
  SUM(u.usage_quantity) AS dbus,  
  SUM(u.usage_quantity * lp.pricing.effective_list.default) AS list_cost  
FROM system.billing.usage u  
JOIN system.billing.list_prices lp  
  ON  u.sku_name = lp.sku_name  
  AND u.usage_end_time >= lp.price_start_time  
  AND (lp.price_end_time IS NULL OR u.usage_end_time < lp.price_end_time)  
WHERE u.billing_origin_product = 'GENIE'  
  AND u.sku_name != 'GENIE_FREE_USAGE'  
GROUP BY  
  u.account_id,  
  u.workspace_id,  
  u.usage_date,  
  u.identity_metadata.run_as,  
  u.usage_metadata.genie.surface,  
  u.usage_metadata.genie.channel,  
  u.sku_name  
ORDER BY u.usage_date DESC
```

### Query free and billed Genie usage per user

To see a monthly running total of per-user free versus billed Genie DBU consumption, use the following query.

note

Free usage, under the `GENIE_FREE_USAGE` SKU, only starts appearing on July 20, 2026. Free usage consumed before this date is not visible in the system tables.

SQL

```
SELECT  
  u.identity_metadata.run_as AS user,  
  u.usage_metadata.genie.surface AS genie_surface,  
  SUM(CASE WHEN u.sku_name = 'GENIE_FREE_USAGE' THEN u.usage_quantity ELSE 0 END) AS free_dbus,  
  SUM(CASE WHEN u.sku_name != 'GENIE_FREE_USAGE' THEN u.usage_quantity ELSE 0 END) AS paid_dbus  
FROM system.billing.usage u  
WHERE u.billing_origin_product = 'GENIE'  
  AND u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)  
GROUP BY  
  u.identity_metadata.run_as,  
  u.usage_metadata.genie.surface  
ORDER BY user, genie_surface
```

This helps you understand which users are consuming free usage (Genie Code free allowance, Genie One, and Genie Agents) versus billed Genie Code usage.

## Understand promotional pricing for Genie

During the promotional period (through January 31, 2027), a 25% discount applies to all billed Genie usage. The discount is automatically factored into the DBU metering. To accurately calculate list cost, multiply the billed usage by `pricing.effective_list.default` from `system.billing.list_prices`. How the discount appears in your billing data depends on the Genie product.

### Genie Code promotional pricing

For Genie Code, the promotional pricing works as follows:

* **Free allowance**: Each user receives 150 free DBUs per month. This usage appears in `system.billing.usage` but is not billed.
* **Billed usage above the free allowance**: The 25% discount is applied directly in the DBU metering, meaning the `usage_quantity` already reflects the discounted consumption. You can multiply directly by the list price to get your list cost, subject to your negotiated discount.

The discount is applied in DBU metering rather than as a separate discounted SKU, because the Serverless Real-Time Inference SKU is shared across multiple product lines. There is no separate discounted SKU for Genie.

### Genie One and Genie Agents promotional pricing

Through July 31, 2026, all Genie One and Genie Agents usage is free. Because these products use the free usage SKU (`GENIE_FREE_USAGE`), no discount or DBU adjustment appears in the billing data. To estimate what this free usage would equal in billed usage, use the query in [Estimate equivalent cost for free Genie usage](#estimate-equivalent-cost-for-free-genie-usage), which includes the 25% discount in the `estimated_list_cost` column.

## Estimate equivalent cost for free Genie usage

If you want to estimate what your free usage (Genie One, Genie Agents, or the Genie Code free allowance) would cost if it were billed at the Genie Code rate, you can resolve a proxy SKU from your workspace's existing billed Genie Code usage and apply that price.

How it works:

1. **Isolate free usage rows**: Filter `system.billing.usage` where `sku_name = 'GENIE_FREE_USAGE'`.
2. **Resolve a proxy regional SKU per workspace**: For each `workspace_id`, find the most recent record in `system.billing.usage` where `billing_origin_product = 'GENIE'` and `sku_name != 'GENIE_FREE_USAGE'`, scoped to the last 30 days to avoid a full history scan. Use that record's `sku_name` as the proxy.
3. **Attach the proxy SKU**: Join the free usage rows to the per-workspace proxy SKU lookup on `workspace_id`.
4. **Price lookup**: Join to `system.billing.list_prices` on the resolved `sku_name`, respecting the price validity window.

The following query returns the estimated cost of free usage, per user, for the current month.

SQL

```
-- Estimate the equivalent billed cost of GENIE_FREE_USAGE rows,  
-- per user and workspace, with the 25% promotional discount applied.  
  
WITH  
  
-- Step 1: Isolate the free-usage rows for the current month  
free_usage AS (  
  SELECT  
    account_id,  
    workspace_id,  
    identity_metadata.run_as AS run_as,  
    usage_metadata.genie.surface AS genie_surface,  
    usage_quantity,  
    usage_end_time  
  FROM system.billing.usage  
  WHERE billing_origin_product = 'GENIE'  
    AND sku_name = 'GENIE_FREE_USAGE'  
    AND usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)  
),  
  
-- Step 2: Find the latest billed GENIE SKU per workspace, scoped to the last 30 days  
latest_real_sku AS (  
  SELECT  
    workspace_id,  
    max_by(sku_name, usage_start_time) AS proxy_sku_name  
  FROM system.billing.usage  
  WHERE billing_origin_product = 'GENIE'  
    AND sku_name != 'GENIE_FREE_USAGE'  
    AND usage_date >= CURRENT_DATE - 30  
  GROUP BY workspace_id  
),  
  
-- Step 3: Attach the proxy SKU to each free-usage row  
resolved AS (  
  SELECT  
    f.account_id,  
    f.workspace_id,  
    f.run_as,  
    f.genie_surface,  
    f.usage_quantity,  
    f.usage_end_time,  
    r.proxy_sku_name AS pricing_sku_name  
  FROM free_usage f  
  LEFT JOIN latest_real_sku r  
    ON f.workspace_id = r.workspace_id  
),  
  
-- Step 4: Join to list prices on the resolved SKU + validity window, applying the 25% promotion  
priced AS (  
  SELECT  
    r.account_id,  
    r.workspace_id,  
    r.run_as AS user,  
    r.genie_surface,  
    r.usage_quantity,  
    lp.pricing.effective_list.default AS list_price_per_unit,  
    r.usage_quantity * lp.pricing.effective_list.default * 0.75 AS estimated_list_cost  
  FROM resolved r  
  LEFT JOIN system.billing.list_prices lp  
    ON  r.pricing_sku_name  = lp.sku_name  
    AND r.usage_end_time    >= lp.price_start_time  
    AND (lp.price_end_time IS NULL OR r.usage_end_time < lp.price_end_time)  
)  
  
-- Step 5: Aggregate per user, per workspace  
SELECT  
  account_id,  
  workspace_id,  
  user,  
  genie_surface,  
  SUM(usage_quantity) AS total_dbus,  
  list_price_per_unit,  
  SUM(estimated_list_cost) AS total_estimated_list_cost  
FROM priced  
GROUP BY account_id, workspace_id, user, genie_surface, list_price_per_unit  
ORDER BY workspace_id, user, genie_surface
```

The `estimated_list_cost` column applies the 25% promotional discount, reflecting what this free usage would cost as billed usage during the promotional period (through January 31, 2027). See [Understand promotional pricing for Genie](#understand-promotional-pricing-for-genie).

note

This query requires that at least one billed Genie Code usage record exists in the workspace. If a workspace has only free usage and no Genie Code usage, the proxy SKU is `NULL` and no price is resolved.

## Additional resources

* [Manage budgets and cost controls for Genie](/aws/en/genie/budgets)
* [Genie cost and budgets FAQ](/aws/en/genie/genie-cost-budgets-faq)
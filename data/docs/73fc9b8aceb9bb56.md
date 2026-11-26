The Lakeflow Designer editor has six areas that work together. The canvas sits in the middle, with panes around it for browsing, configuring, and checking your work:

* **[Header and toolbar](#header)**: Pick compute, schedule the visual data prep, control previews, and move around the canvas.
* **[Left pane](#left-pane)**: Browse operators, the table of contents, workspace files, catalog data, and parameters.
* **[Canvas](#canvas)**: Add operators and connect them to build a visual data prep.
* **[Configuration pane](#configuration-pane)**: Configure the selected operator. It opens on the right.
* **[Output pane](#output-pane)**: Check the selected operator's input and output data. It opens at the bottom.
* **[Genie Code prompt](#genie-code)**: Describe changes in natural language. It floats above the canvas.

In the image above, you can see:

1. [The left pane](#left-pane), with the **Operators**, **Table of contents**, and **Parameters** panes
2. [An operator](/aws/en/designer/what-is-lakeflow-designer#operators)
3. [A connection between two operators](#connect)
4. [The drag-and-drop canvas](#canvas)
5. [The Genie Code prompt](#genie-code)
6. [The output pane](#output-pane)
7. [The data profile of the output](/aws/en/designer/preview-results#data-profile)

## Header and toolbar

The header at the top of the editor holds the file name and file-level actions:

* **Compute picker**: Select the compute for the visual data prep. The picker is next to the **Schedule** button. See [Prerequisites](/aws/en/designer/build-transformation#prerequisites).
* **Schedule**: Create a scheduled job for the visual data prep. See [Schedule as a job](/aws/en/designer/production#schedule).
* **kebab menu**: Export the file, run or clear the whole visual data prep from the **Run** menu, and use other file actions. See [Manage visual data prep files in Lakeflow Designer](/aws/en/designer/manage-files) and [Run the full visual data prep](/aws/en/designer/preview-results#run-all).

The toolbar above the canvas holds editing and canvas controls:

* **Preview**: Set how many rows operators process for previews. See [Control how much data previews process](/aws/en/designer/preview-results#preview).
* **Run all**: Run every operator on the full dataset. See [Run the full visual data prep](/aws/en/designer/preview-results#run-all).
* **Undo and redo**: Undo or redo changes to the visual data prep. You can also press **Cmd/Ctrl+Z** and **Cmd/Ctrl+Shift+Z**.
* **Canvas controls**: Zoom, fit the view, auto-layout, and drag mode. See [Navigate the canvas](#navigate).

* **Apps**: Create, open, and publish Designer Apps for the visual data prep. See [Build and publish a Designer App](/aws/en/designer/build-publish-app).

## Left pane

The left pane holds the following panes:

* **Operators**: Browse and search the [built-in operators](/aws/en/designer/built-in-operators) and your [custom operators](/aws/en/designer/user-operators). Search understands intent, so typing `average by month` returns the **Aggregate** operator. Click an operator, or drag it onto the canvas, to add it.
* **Table of contents**: Find any operator in the visual data prep, filter and sort the list, and view each operator's generated code. See [Use the table of contents in Lakeflow Designer](/aws/en/designer/table-of-contents).
* **Workspace**: Browse the workspace file system. Drag a CSV or Excel file onto the canvas to add it as a source. See [Drag and drop a file](/aws/en/designer/ingest-data#drag-drop).
* **Catalog**: Browse Unity Catalog catalogs, schemas, and tables. Drag a table onto the canvas to add it as a source.
* **Parameters**: Define and manage [parameters](/aws/en/designer/parameters) for the visual data prep.

## Canvas

The canvas is where you build a visual data prep. Operators appear as boxes on the canvas, and connections between them show how data flows from left to right.

### Add operators

Use any of the following methods to add an operator:

* In the **Operators** pane, click an operator, or drag it onto the canvas.
* Click the  button next to an existing operator to add a new operator that's already connected to it.
* Right-click the canvas and add an operator from the shortcut menu.

An unconfigured operator has a dashed border. For details on each operator, see [Built-in operators in Lakeflow Designer](/aws/en/designer/built-in-operators).

### Connect operators

To connect two operators, drag from the output port on the right edge of an operator to the input port on the left edge of the next operator. Data flows from the first operator into the second.

Some operators, such as **Join** and **Combine**, accept multiple input connections. A required input port that isn't connected is highlighted in yellow.

To remove a connection, hover over it and click  in the toolbar that appears over the connection.

Select an operator to highlight its lineage on the canvas. The connections back to its upstream sources and forward to its downstream outputs are highlighted, so you can follow how data reaches and leaves that operator.

### Rename, copy, delete, and disable operators

After an operator is on the canvas, you can act on it as follows:

* **Rename an operator**: Click the box at the top of the configuration pane to rename the operator. Descriptive names make your visual data prep easier to understand at a glance. Some operators, such as the [SQL operator](/aws/en/designer/built-in-operators#sql), can reference the output of other operators by name.
* **Copy an operator**: Hover over an operator and click , or select an operator and press **Cmd/Ctrl+C** then **Cmd/Ctrl+V**.
* **Delete an operator**: Hover over an operator and click  in the toolbar that appears above it, or select the operator and press **Delete**.
* **Delete and reconnect**: Right-click an operator and select **Delete and reconnect** to remove it and connect its upstream output directly to its downstream operators. You need edit access. The action applies to one operator at a time and requires one distinct upstream output and at least one downstream connection. If the connection requirements are unmet, hover over  next to **Delete and reconnect** for the reason. Update any SQL expressions that refer to the deleted operator by name.
* **Enable or disable an operator**: Right-click an operator, or a group, and select **Disable** to exclude it from runs, or **Enable** to include it again. A disabled operator produces no output rows, so downstream operators receive an empty result until you enable it. To disable an operator based on a parameter, see [Enable or disable an operator with a parameter](/aws/en/designer/parameters#enable-disable).
* **Favorite an operator**: Right-click an operator and select **Favorite** to mark it as a favorite, or **Unfavorite** to remove it. Favorited operators show a badge on the canvas. See [Sort and filter the list](/aws/en/designer/table-of-contents#sort-filter).
* **Group operators**: Use the [Group](/aws/en/designer/built-in-operators#group) operator to organize related operators on the canvas.
* **Add a note**: Use the [Note](/aws/en/designer/built-in-operators#note) operator to document the workflow on the canvas.

### Navigate the canvas

Use the following controls to move around the canvas and arrange operators:

* **Constrain a drag**: Hold **Shift** while dragging an operator or a selection to constrain movement to the horizontal or vertical axis.
* **Pan**: Hold **Space** while clicking and dragging, or slide two fingers on a trackpad.
* **Zoom**: Pinch or stretch on a trackpad, or hold **Ctrl** and scroll. You can also click  or  in the toolbar.
* **Drag mode**: Click  in the toolbar to turn drag mode on or off.
* **Auto-layout**: Click  in the toolbar to automatically arrange all operators in a compact layout.
* **Fit view**: Click  in the toolbar to see all operators in the current viewport.
* **Shortcut menu**: Right-click anywhere on the canvas to access common actions, including adding operators, undo and redo, auto-layout, fit view, and opening the code pane.
* **Command palette**: Press **Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows to access editor actions.

### Discuss work with canvas comments

Canvas comments keep a discussion attached to an operator or a position on the canvas. To start a thread:

1. Right-click an operator or the canvas and select **Add comment**.
2. Enter your message and click **Comment**.
3. Open the comment pin to read the thread. Enter a response and click **Reply** to continue the discussion.

Click  (**Comments**) in the header to open the comments pane. Use **Open** and **Resolved** to find threads by status. Editors can click  (**Resolve comment**) when a discussion is complete, or  (**Reopen comment**) to continue it. Viewers can reply without permission to edit the visual data prep. Job-run views do not allow replies.

## Configuration pane

The configuration pane is where you fill in the details of an operator, such as the columns to join on or the condition to filter by. To open it, double-click an operator, or hover over it and click  (**Edit operator**). Set the options for that operator type, then click **Apply**. For the Aggregate, Prepare, Limit, Sort, AI Function, and Geospatial operators, and for the Pivot operator in **Columns → Rows** mode, missing required settings disable **Apply**. Hover over **Apply** to see which settings to complete.

For a larger editing area in a supported expression field:

1. Click  (**Expand editor**) next to the expression editor.
2. Edit the expression. To browse input columns and SQL functions, select **Show columns and functions** and search the reference list.
3. Select a column or function from the list to insert it at the cursor.
4. Click **Done** to return to the configuration pane.

Each operator also shows an AI-generated description of what it does. Editing the description reconfigures the operator to match. To change an operator by describing what you want, click **Edit with Genie Code** in the configuration pane. See [Use Genie Code in Lakeflow Designer](/aws/en/designer/genie-code).

## Output pane

The output pane opens at the bottom of the editor when you select an operator. It shows the operator's input and output data, or renders non-table results such as plots, HTML, and images. You can edit data directly in the preview, open a data profile, and download results. See [Preview and refine results in Lakeflow Designer](/aws/en/designer/preview-results).

## Genie Code prompt

The Genie Code prompt floats above the canvas. Type a request in natural language, and Genie Code adds or changes operators on the canvas.

prompt

For example, tell Genie Code:

Text

```
Remove rows where the email is null.
```

A one-line summary of its most recent edit appears above the input box. To open the full conversation history, click . See [Use Genie Code in Lakeflow Designer](/aws/en/designer/genie-code).

## Additional resources

* [Tutorial: Build a visual data prep](/aws/en/designer/build-transformation)
* [Use Genie Code in Lakeflow Designer](/aws/en/designer/genie-code)
* [Use the table of contents in Lakeflow Designer](/aws/en/designer/table-of-contents)
* [Preview and refine results in Lakeflow Designer](/aws/en/designer/preview-results)
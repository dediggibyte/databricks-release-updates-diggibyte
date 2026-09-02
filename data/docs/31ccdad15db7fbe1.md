Chat in Genie One is a unified, full-screen natural-language interface for business users to ask data questions. It first searches available Genie Agents for a match, then searches across dashboards, queries, and metric views. You can also connect external sources (such as Google Drive and SharePoint) so chat can answer from your company documents and schedule recurring chat tasks that post results back as a thread.

## How chat works

When you submit a question to chat:

1. It searches available Genie Agents for one relevant to your question.
2. If a matching Genie Agent is found, it uses that space to generate a response.
3. If no matching Genie Agent is found, it searches for relevant data assets to answer your question.

To give chat access to your company documents, connect external data sources such as Google Drive, SharePoint, GitHub, Glean, and Atlassian. See [Connect to external tools and sources](/aws/en/genie-one/external-sources).

To open chat, click **New chat** from the sidebar or use **Ask** mode in the search bar. You must have the CAN USE permission on at least one SQL warehouse to use chat.

### Select a level of effort

After you open a chat in a Databricks workspace, the selector in the prompt box shows the current level of effort and lets you change it:

* **Auto** (default, recommended): This level provides the highest quality for any task.
* **Low**: This level lowers the cost for simpler tasks.

The level of effort applies only to workspace chat. It does not affect account-level chat, Genie Agent threads, or dashboard contexts.

### Select compute

Chat uses **Auto** compute by default, which automatically selects the best available SQL warehouse and is recommended for most users. To use a specific warehouse instead:

1. Click **•••** in the top right.
2. Click **Manage compute**.
3. Select your SQL warehouse.

## Manage chats in the sidebar

Your recent chats appear in the sidebar. Hover over a chat and click the  kebab menu to manage it:

* **Pin a chat**: Select **Pin** to keep the chat at the top of the sidebar for quick access. Pinned chats stay at the top until you unpin them.
* **Rename a chat**: Select **Rename**, enter a new name, and confirm to give the chat a clearer title.

## Create a Genie Agent from a conversation

You can turn the context from a chat conversation into a reusable Genie Agent. This is helpful when a conversation builds up context that you want to save and apply to future questions, such as a sales KPI analysis, business report formatting guidance, or other domain-specific instructions.

note

To create a Genie Agent from Genie One, you must have the **Workspace access** or **Databricks SQL access** entitlement. Users with only **Consumer access** and account users without workspace membership can't create Genie Agents from Genie One. See [Manage entitlements](/aws/en/security/auth/entitlements).

### Create an agent

You can create a Genie Agent from a conversation in two ways:

* Ask Genie One to save the conversation's context as an agent.
* Click the overflow menu (**•••**) under an answer, then click **Create Agent**.

To create an agent in a conversation, tell Genie One what you want the agent to capture:

prompt

```
Save this sales KPI analysis as an agent so I can reuse it.
```

After Genie One creates the agent, you can open it in your workspace to fine-tune its context, instructions, and data assets. To learn more about Genie Agents, see [Genie Agents](/aws/en/genie-agents/).

### Edit an agent

You can ask Genie One to change an agent's context in a conversation. For example, you can add tables or change an agent's instructions in natural language.

prompt

```
Add the sales.forecast table to my sales KPI agent.
```

### Delete an agent

You can ask Genie One to delete an agent in a conversation. Genie One asks you to confirm before it deletes the agent.

prompt

```
Delete my sales KPI agent.
```

## Genie Ontology

Public Preview

This feature is in [Public Preview](/aws/en/release-notes/release-types).

The Genie Ontology is the unified context layer that gives Genie One a business-aware map of your organization. It brings together two categories of context:

* **Unity Catalog semantics**: Modeled context that you define, govern, and certify through features like [metric views](/aws/en/uc-semantics/metric-views/), [domains](/aws/en/uc-semantics/domains), and [Pages](/aws/en/uc-semantics/pages).
* **Inferred context**: A map of snippets that Genie automatically extracts and maintains from your existing assets and usage, including metric views, dashboards, SQL queries, and Genie Agents.

For example, inferred snippets can include:

* **Metric definitions**: For example, "An 'active user' is a distinct user, deduplicated across all platforms."
* **Authoritative sources**: For example, "Revenue questions should be answered using the curated Finance Genie Agent."
* **Business rules**: For example, "A 'qualified lead' only counts once a demo is booked."

Each snippet gets an authority score based on where it was generated from, how often it is used, and how fresh it is. Snippets are also gated using Unity Catalog permissions. When you ask a question, Genie One ranks the most relevant snippets, resolves conflicts, and answers using only the sources you are permitted to see. This generates more accurate responses and reduces latency by reducing the amount of data Genie One needs to crawl and query.

To see which knowledge sources Genie One used to answer your question, click the  citation icons in a response.

Genie Code searches the same ontology, so context curated once applies to both surfaces. See [Genie Ontology](/aws/en/genie-code/use-genie-code#ontology).

note

At this time, customers do not incur costs for curating ontology snippets. However, Databricks may update pricing for the feature at any time by notifying you and/or by updating our [pricing page](https://www.databricks.com/product/pricing).

## Add workspace instructions for chat

Workspace admins can add custom instructions that apply to every chat conversation in the workspace. Instructions can include information about your organization's data conventions, preferred terminology, or guidelines for how chat should respond.

To add workspace instructions, create a Markdown file at the following path in your workspace:

```
/Workspace/.genie_workspace_instructions.md
```

Instructions must be under 20,000 characters. Chat reads this file automatically with no additional configuration required. Instructions apply to chat only and do not affect Genie Agents or Genie Code.

For best practices on adding custom instructions, see [Best practices for Genie Code instructions](/aws/en/genie-code/instructions#limits).

## User skills

User skills let you extend chat in Genie One with custom capabilities tailored to your personal needs. Skills are available only to you and are loaded automatically when Genie One determines they are relevant to your request. You can also invoke a skill manually by typing `/` followed by its name.

note

For agent skills in Genie Code, see [Extend Genie Code with agent skills](/aws/en/genie-code/skills).

### Create a user skill

prompt

Tell Genie One to do this for you:

```
Create a user skill that summarizes weekly sales trends for my region.
```

Genie One creates the skill and saves it to your workspace at `/Workspace/Users/{email}/.assistant/skills/`.

### Edit a user skill

To edit a user skill, ask Genie One to make changes in a conversation, or open the skill in Canvas and edit it directly.

To rename or delete a user skill, access the skill file directly in your workspace at `/Workspace/Users/{email}/.assistant/skills/`.

### Invoke a user skill

Genie One automatically loads skills when they are relevant to your request. To invoke a skill, type `/` followed by its name in the chat input.

## Scheduled tasks

Scheduled tasks run automatically at a specified time and post the results in a chat thread. When a task runs, chat sends you an email with the results, including any visualizations, and a PDF attachment of the task's output.

You can create a scheduled task in two ways:

* Type a request in natural language in chat, for example: *"Send me a daily briefing of all new customer reviews for my store location."* Chat might ask clarifying questions, such as the time or which location to use, then creates the task and adds it to the **Schedules** section.
* In the sidebar, click **Schedules**, then click the drop-down menu next to **+ Create in chat** and select **Create manually**.

  Fill in the **Title**, **Instructions**, **Connections**, **Schedule**, and **Timezone**, then click **Create**.

To view past runs, edit, or delete a scheduled task, click the task in the **Scheduled tasks** section. Each run opens in a chat thread.

When you author a scheduled task, select **Run now** to run it immediately without waiting for the next scheduled time.

To reference a scheduled task in a new request, @mention it in chat.

## Recall past conversations

Genie One remembers your past conversations and can draw on them to shape its answers, so you can build on earlier work without repeating yourself. Genie One only references your own conversations. This capability is always available and requires no setup.

Most of the time, Genie One draws on your conversation history automatically when earlier context is relevant, rather than only when you ask it to recall a past thread. When a previous conversation is used for context, it adds a citation that links back to the original conversation, just like any other source.

You can also draw on your past conversations yourself in two ways:

* **Bring past context into your current conversation.** Reference an earlier conversation to pull its context into the chat you're already in, without navigating away.
* **Find and reopen a past conversation.** Search by content to locate an earlier conversation, then reopen it to continue that thread.

For example, to drill down from a past conversation without leaving your current one:

prompt

```
Remember when we talked about ARR last quarter? Let's drill down from that conversation and break it out by region.
```

## Add to Genie One's memory

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To access it, a workspace admin must enable the **Genie One Memory** preview from the workspace [Previews page](/aws/en/admin/workspace-settings/manage-previews).

Genie One can retain specific facts you provide as memories and apply them in later conversations, so you don't need to repeat the same context every time you chat. Genie One's memories are private to you and aren't shared with other users.

Genie One saves a memory only when you explicitly ask it to. To create a memory, tell Genie One what to remember in a conversation:

prompt

```
Remember that I report all revenue in USD and my fiscal year starts in February.
```

Genie One automatically applies your saved memories to future conversations.

When Genie One applies a memory, it includes a citation for the memory it used. You can give that memory a thumbs-up or thumbs-down to let Genie One know whether it's helpful. If a memory is wrong or out of date, ask Genie One to update or delete it directly in a conversation.

## Upload a file

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To access it, a workspace admin must enable the **Genie One File Upload** preview from the workspace [Previews page](/aws/en/admin/workspace-settings/manage-previews).

Upload CSV, Excel, PDF, image, and Word files directly into a chat conversation to analyze them in natural language alongside your other data. Uploaded files are private to the conversation you add them to, and only you can access them.

To upload a file, select  in the message composer, then  **Add files**. You can also drag and drop files onto the composer or paste them from your clipboard. To see the files in a conversation, select  and open the **Uploaded files** list.

File requirements:

* Each CSV or Excel file must be smaller than 200 MB. An Excel file can contain multiple sheets. To query a specific sheet, reference it by name.
* Each PDF must be smaller than 20 MB and contain no more than 20 pages. Genie One reads up to 4,000 characters per page.
* Each image (PNG, JPG, or JPEG) must be smaller than 5 MB. Genie One automatically downscales larger images.
* You can upload Word (`.docx`) files.
* You can upload up to 100 files per conversation, and up to 5 files in a single action.

Databricks stores uploaded files in a Unity Catalog managed volume, in customer-managed root storage on classic workspaces or in [default storage](/aws/en/storage/default-storage) on serverless workspaces. For details, see  [Upload a file](/aws/en/genie-agents/file-upload#upload).

Uploaded files have no fixed retention period and no configurable lifecycle policy. They remain until you remove them or delete the conversation. For details, see  [Remove a file](/aws/en/genie-agents/file-upload#remove).

## Search the web

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To use it, a workspace admin must turn on **Web search in Genie Code and Genie One** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

Genie One can search the public web to answer questions that need current information, such as recent release notes, third-party documentation, or news. Genie One decides when to search based on your request and cites the sources it uses. Each source appears in the response as a link you can open.

Web search has the following requirements:

* The workspace must have [partner-powered AI features](/aws/en/databricks-ai/partner-powered) enabled.
* The workspace must be in an eligible geo (Americas or Europe), or have [cross-geography processing enabled](/aws/en/resources/databricks-geos#cross-geo-proc
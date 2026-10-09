Chat in Genie One is a unified, full-screen natural-language interface for business users to ask data questions. It first searches available Genie Agents for a match, then searches across dashboards, queries, and metric views. You can also connect external sources (such as Google Drive and SharePoint) so chat can answer from your company documents and schedule recurring chat tasks that post results back as a thread.

## How chat works

When you submit a question to chat:

1. It searches available Genie Agents for one relevant to your question.
2. If a matching Genie Agent is found, it uses that space to generate a response.
3. If no matching Genie Agent is found, it searches for relevant data assets to answer your question.

To give chat access to your company documents, connect external data sources such as Google Drive, SharePoint, GitHub, Glean, and Atlassian. See [Connect Genie One to external tools and sources](/aws/en/genie-one/external-sources).

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

Genie One uses Genie Ontology, the unified context layer that gives Genie a business-aware map of your organization. It combines modeled context you govern in Unity Catalog semantics, such as metric views, domains, and Pages, with context Genie infers automatically from your assets and usage. Genie One and Genie Code search the same ontology, so context you curate once applies to both surfaces.

To see which knowledge sources Genie One used to answer your question, click the  citation icons in a response.

For a full description of Genie Ontology, including inferred context, authority scoring, and permission gating, see [Genie Ontology](/aws/en/genie/genie-ontology).

## Add workspace instructions for chat

Workspace admins can add custom instructions that apply to every chat conversation in the workspace. Instructions can include information about your organization's data conventions, preferred terminology, or guidelines for how chat should respond.

To add workspace instructions, create a Markdown file at the following path in your workspace:

```
/Workspace/.genie_workspace_instructions.md
```

Instructions must be under 20,000 characters. Chat reads this file automatically with no additional configuration required. Instructions apply to chat only and do not affect Genie Agents or Genie Code.

For best practices on adding custom instructions, see [Best practices for Genie Code instructions](/aws/en/genie-code/instructions#limits).

## Skills

Skills let you extend chat in Genie One with custom capabilities tailored to your needs. By default, a skill is available only to you, but you can share it with your team. See [Share a skill with your team](#share-skills). Skills are loaded automatically when Genie One determines they are relevant to your request, and you can invoke a skill manually by typing `/` followed by its name.

A skill can include multiple files and sub-folders, up to three folders deep and 50 files or folders per skill. Skills can contain text files only. Images, PDFs, and other binary files are not supported.

note

For agent skills in Genie Code, see [Extend Genie Code with agent skills](/aws/en/genie-code/skills).

### Create a skill

prompt

Tell Genie One to do this for you:

```
Create a skill that summarizes weekly sales trends for my region.
```

Genie One creates the skill and saves it to your workspace at `/Workspace/Users/{email}/.assistant/skills/`.

### Edit a skill

To edit a skill, ask Genie One to make changes in a conversation, then review the changes in the sidebar. You can also manage a skill from its page:

1. In the left navigation, click **Customizations**, then click **Skills**.
2. Select the skill.
3. From the drop-down menu next to **Share** in the top right, select **Edit with Genie** to change the skill in a conversation, or **Open in workspace editor** to edit its files directly.

To delete a skill, follow the same steps and select **Remove skill** from the drop-down menu.

### Invoke a skill

Genie One automatically loads skills when they are relevant to your request. To invoke a skill, type `/` followed by its name in the chat input.

### Share a skill with your team

Beta

This feature is in [Beta](/aws/en/release-notes/release-types) and requires two previews:

* An account admin must turn on the **Enhanced Unity AI Gateway** preview from the account console [Previews page](/aws/en/admin/workspace-settings/manage-previews#account).
* A workspace admin must turn on the **Unity Gateway skills in Genie** preview from the workspace [Previews page](/aws/en/admin/workspace-settings/manage-previews#workspace).

You can publish a skill and share it with teammates. Skills are governed by Unity Gateway, so the same catalog and schema privileges that protect your other data control who can publish and use them:

* To publish a skill, you need `USE CATALOG`, `USE SCHEMA`, and `CREATE VOLUME` on the target schema.
* To install and use a shared skill, you need `USE CATALOG`, `USE SCHEMA`, and `READ VOLUME` on the schema that holds it.

For the full privilege model, including the privileges needed to update a published skill, see [Grant access to skills](/aws/en/ai-gateway/govern-skills#grant-access).

To publish a skill and share it:

1. In the left navigation, click **Customizations**, then click **Skills**.
2. Select the skill, then click **Share**.
3. Under **Publish to**, select a catalog and schema.
4. Add the users, groups, or service principals to share with, and set the general access level.
5. Click **Done**.

### Find and install shared skills

On the customization page, skills that teammates shared with you appear next to your skills. Install a skill to use it in your chats, and uninstall it to stop using it.

You can also browse skills from chat: click **+** in the message composer, then select **Skills** > **Browse skills**.

### Use shared skills in scheduled tasks

Skills you install are available in [scheduled tasks](#scheduled-tasks), including tasks shared with your team, so recurring runs apply the same skills.

### Skill limitations

Uploading files to a skill isn't supported in the Genie One UI. To add files, upload them from Catalog Explorer the same way you would for a volume: click  **Catalog**, browse to the skill in the catalog and schema you published it to, then upload your files. See [Use Catalog Explorer](/aws/en/volumes/volume-files#use-catalog-explorer).

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

## Personalized starter questions

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To use it, a workspace admin must turn on **Personalized Genie One Starter Questions** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

When personalized starter questions are enabled, the Genie One home page shows a small number of suggested questions tailored to you. Each one is a single-line prompt. Select a question to open a chat with it already entered, so you can start exploring your data.

### How questions are personalized

Genie One generates starter questions for you from your own recent Databricks activity: the tables, AI/BI dashboards, Genie Agents, and notebooks that you frequently use, recently viewed, or marked as favorites. If you have little recent activity, Genie One suggests questions based on assets that are popular across your workspace instead.

### Data access and privacy

Starter questions only reference assets that you already have access to. They are generated using your own permissions, so they never surface data outside your access. Generation uses only asset metadata, such as names and types. It never reads the contents of your tables, dashboards, or notebooks.

### Availability

Personalized starter questions are in Beta. Workspace admins control access from the **Previews** page, as noted at the start of this section. When the feature is not enabled for a workspace, the home page shows a small set of generic default starter questions instead.

### Limitations for personalized starter questions

Personalized starter questions are cached for each user and refresh periodically, so they might not reflect your most recent activity immediately.

For more about Genie One, see [Use Genie One](/aws/en/genie-one/).

## Add to Genie One's memory

Genie One can retain specific facts you provide as memories and apply them in later conversations, so you don't need to repeat the same context every time you chat. Genie One's memories are private to you and aren't shared with other users.

Genie One saves a memory when you explicitly ask it to. To create a memory, tell Genie One what to remember in a conversation:

prompt

```
Remember that I r
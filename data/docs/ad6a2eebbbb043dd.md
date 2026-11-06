Preview

This feature is in [Public Preview](/aws/en/release-notes/release-types). Account admins can manage access to this feature from the account console **Previews** page. See  [Manage account-level previews](/aws/en/admin/workspace-settings/manage-previews#account).

The Databricks Genie app in Microsoft Teams brings [Genie](/aws/en/genie-one/chat) into Microsoft Teams so users can ask data questions and get answers without leaving the Microsoft Teams workspace. Users can chat with the app in a direct message or mention `@Databricks Genie` in a Microsoft Teams channel or group chat. Questions are answered by Genie One or by a specific Genie Agent pinned in a direct message or channel for consistent, use-case-specific answers.

When a Genie Agent is pinned, new conversations go directly to that agent in [Agent mode](/aws/en/genie-agents/concepts#agent-mode) through the [Agent mode API](https://docs.databricks.com/api/genie/v1/agent-mode-create-response). Otherwise, the Databricks Genie app in Microsoft Teams uses the Genie One API. The app uses the same model providers and trust and safety guarantees as Genie. See [Hosting provider used when partner-powered AI features setting is enabled and disabled](/aws/en/databricks-ai/partner-powered#features) and [Databricks AI assistive features trust and safety](/aws/en/databricks-ai/databricks-ai-trust).

This page describes how to download, set up, and use the Databricks Genie app in Microsoft Teams.

important

Databricks agents may generate inaccurate responses. Verify before acting on agent output.

## Prerequisites

Before installing the Databricks Genie app in Microsoft Teams:

* An account admin must enable the **Databricks Genie for Microsoft Teams** preview in the account console.
* To upload files in direct messages, each user's Microsoft Teams account must have OneDrive for Business. See [Upload files](#upload-files).
* To let users save documents as PDFs in direct messages, each user needs OneDrive and version 1.0.17 and above of the Databricks Genie app in Microsoft Teams. See [Save documents as PDFs](#save-pdf).
* If your workspace uses an IP access list, add the outbound IPs of the Databricks control plane in the East US 2 region. See the Outbound IPs in [the Azure Databricks documentation](https://learn.microsoft.com/azure/databricks/resources/ip-domain-region#outbound).
* If your workspace uses Private Link, an account admin must add a context-based ingress rule that allows the app. See [Use with Private Link workspaces](#private-link).

## Install the Databricks Genie app in Microsoft Teams

A Microsoft 365 admin installs the Databricks Genie app in Microsoft Teams from the Microsoft marketplace:

1. In the Microsoft marketplace, search for and find **Databricks Genie**.
2. Install the app.
3. Approve the app permissions when prompted during installation.

For a list of required permissions, see  [Required app permissions on Microsoft](#app-permissions).

After installation, users can start using the app.

## Use the Databricks Genie app in Microsoft Teams

You can use the Databricks Genie app in Microsoft Teams through direct messages or in channel conversations on your Microsoft Teams workspace, or from [Microsoft 365 Copilot](/aws/en/integrations/msft-m365-copilot).

### Direct message

To directly message the Databricks Genie app in Microsoft Teams:

1. In Microsoft Teams, click **Apps** in the left sidebar and open the Databricks Genie app in Microsoft Teams.
2. Enter your question.
3. If you are not signed in, the Databricks Genie app in Microsoft Teams prompts you to sign in:

   1. Click **Configure**.
   2. Specify your **Workspace URL**. To find your workspace URL, see [Workspace instance names, URLs, and IDs](/aws/en/workspace/workspace-details#workspace-url).
   3. Click **Continue** to log in to your Databricks account.
4. Your question is routed to the most appropriate Genie Agent and returns an answer with sources and suggested follow-up prompts.

To start a new conversation in a direct message, send `newchat`. This clears the current conversation context so that your next message starts a new Genie conversation. Your existing Microsoft Teams messages are not deleted.

To configure the workspace and Genie scope for all subsequent direct message conversations, open the Databricks Genie app in the Microsoft Teams home page and adjust the settings.

### Schedule tasks from a direct message

You can create a [scheduled task](/aws/en/genie-one/chat#scheduled-tasks) from a direct message with the Databricks Genie app in Microsoft Teams. Use either of the following methods:

* Ask Genie to schedule it. At any point in the conversation, type a request in natural language, for example: *"Create a daily schedule that pulls the latest customer spend."* Genie might ask clarifying questions, such as the time or time zone, then creates the task.
* Click the scheduling suggestion. When Genie suggests running an answer on a schedule, it shows a **Want to run this analysis on a schedule?** button below the answer. Click the button. Genie asks what the task should do and when it should run, then creates the task.

When the task runs, the Databricks Genie app in Microsoft Teams sends the results to you in a direct message. To continue the conversation about the results, click **Ask a follow up**.

### Upload files

In a direct message, you can attach up to five PDF, Word, or CSV files of 20 MiB or smaller to a message, and Genie uses them as context when it answers. File upload is not available in channels, group chats, Microsoft 365 Copilot, or conversations with a pinned Genie Agent.

Microsoft Teams stores files that you attach in a chat in your OneDrive for Business, so your Microsoft Teams account must have OneDrive for Business to upload files.

To upload files:

1. In a direct message with the Databricks Genie app in Microsoft Teams, attach up to five files to your message.
2. Optionally, enter a question about the files.
3. Send the message.

If your message includes a question, Genie uploads the files and then answers the question using them. If you send files without a question, Genie uploads them and confirms when they are ready. You can then ask questions about the files.

Uploaded files stay available for follow-up questions in the current conversation. After you send `newchat`, attach the files again to use them in the new conversation.

If you attach more than five files, Genie uploads the first five and lists the files it skipped. If a file can't be uploaded, Genie lists it with the reason. As long as at least one file uploads, Genie still answers your question.

If Genie replies that Databricks couldn't authorize the upload, reconnect Databricks and try again. If it still fails, ask a workspace admin to check your file upload permissions.

### Save documents as PDFs

When Genie drafts a document in a direct message, the Databricks Genie app in Microsoft Teams offers the document as a PDF on a file card. To learn how to ask Genie to draft a document, see [Documents in Genie One](/aws/en/genie-one/documents).

To save the PDF to your OneDrive, click **Allow** on the file card. The app replaces the card with the PDF in the chat. To dismiss the offer, click **Decline**.

To save PDFs, you need OneDrive and version 1.0.17 and above of the Databricks Genie app in Microsoft Teams. If clicking **Allow** fails because OneDrive is disabled for your account, open the document in Genie One instead.

* The PDF is named after the document's title.
* If a response includes more than one document, the app offers only the first one.
* The offer expires 15 minutes after the app posts it. If PDF delivery is busy or can't start, the card asks you to click **Allow** again. Do so before the offer expires. To get a PDF after the offer expires, ask Genie to generate the document again.
* PDFs larger than 20 MiB can't be saved. Open the document in Genie One instead.

### Channel conversation

You can add the Databricks Genie app in Microsoft Teams to a channel. Using `config`, channel owners can configure settings for all members of a channel and individual users can configure personal settings. Channel owner configurations override personal configurations.

To configure the Databricks Genie app in Microsoft Teams in a channel:

1. In the desired channel, type `@Databricks Genie`.
2. If prompted, add the Databricks Genie app in Microsoft Teams to the channel.
3. Type `config`.
4. Select the connected workspace, the message visibility, and the Genie scope (Genie One or a specific Genie Agent).

   If no Genie Agent is pinned, the channel defaults to Genie One.
5. After configuration, all `@Databricks Genie` mentions in the channel route to the configured agent and workspace.

### Visualizations

When a Genie response includes a visualization, the chart appears as an image in the reply.

### Approve tool actions

Genie can use [connected external tools](/aws/en/genie-one/external-sources) to answer questions and take actions. When a tool call requires approval, Genie shows an approval card in the reply. Click **Allow** to let Genie run the tool, or **Deny** to stop it. If the card includes a scope selector, choose whether the approval applies **Once**, **Always in this chat**, or **Always**. Only the user who asked the question can approve or deny the request.

## Configuration levels and overrides

Run `config` in a channel to open the configuration window. The following settings are configurable:

* **Workspace Selection**: The Databricks workspace the Databricks Genie app in Microsoft Teams connects to for answering questions.
* **Message visibility**: Whether `@Databricks Genie` responses in channels are visible to all channel members or only to the user who asked. By default, responses are public.
* **Genie scope**: Genie One or a specific Genie Agent. New conversations go directly to a pinned agent in [Agent mode](/aws/en/genie-agents/concepts#agent-mode), and feedback on its answers goes to that agent. A pin in a direct message also applies in Microsoft 365 Copilot. In a channel or group chat, only a channel-wide pin (**Save as channel-wide setting**) routes conversations to the agent. A personal configuration in a channel uses Genie One.

Message visibility settings can be set at three levels. Higher levels override lower levels:

| Level | How to set it | Applies to | Precedence |
| --- | --- | --- | --- |
| Workspace | Databricks workspace admin configures from workspace security settings using the **Allowed collaboration platforms** and **Allow public messages in collaboration platforms** settings.  When **Allow public messages in collaboration platforms** is off, all responses are private to the user who asked. | All channels in the Microsoft Teams workspace | Highest, overrides channel and personal configurations |
| Channel | Channel owner sends `config` in the channel and selects **Save as channel-wide setting** | All members in that channel | Overrides personal configurations |
| Personal | Individual user sends `config` in the channel | That user's own `@Databricks Genie` mentions in the channel | Used when no channel-wide configuration is set |

←✕

| Level | How to set it | Applies to | Precedence |
| --- | --- | --- | --- |
| Workspace | Databricks workspace admin configures from workspace security settings using the **Allowed collaboration platforms** and **Allow public messages in collaboration platforms** settings.  When **Allow public messages in collaboration platforms** is off, all responses are private to the user who asked. | All channels in the Microsoft Teams workspace | Highest, overrides channel and personal configurations |
| Channel | Channel owner sends `config` in the channel and selects **Save as channel-wide setting** | All members in that channel | Overrides personal configurations |
| Personal | Individual user sends `config` in the channel | That user's own `@Databricks Genie` mentions in the channel | Used when no channel-wide configuration is set |

### Workspace admin settings

From **Settings** > **Security** > **External access**, a workspace admin controls whether the Databricks Genie app in Microsoft Teams can connect to the workspace and whether its responses can be public:

* **Allowed collaboration platforms**: Which collaboration platforms can connect to the workspace. Select **Allow all** (the default), **Allow Slack only**, **Allow Teams only**, or **Deny all**. When Microsoft Teams isn't allowed, users can't connect the app to the workspace. Users who are already connected get a private message that connection to the workspace isn't allowed and are asked to change their workspace or contact a workspace admin.
* **Allow public messages in collaboration platforms**: When on, users and channel owners choose whether responses are public or private. When off, responses are visible only to the user who asked.

Changes to these settings can take up to an hour to take effect.

## Data routing

Genie processes your questions in your workspace and stores conversation history in your workspace's region. Requests between Microsoft Teams and your workspace pass through a central Databricks service in the Databricks control plane. The central service runs in the East US 2 region, regardless of your workspace's region. The central service doesn't persist or log any request or answer content. It stores only the mapping between your Microsoft Teams tenant and your Databricks workspace.

Microsoft Teams needs a fixed endpoint to receive requests, so the app uses a central service.

When you ask a question in Microsoft Teams:

1. Microsoft Teams sends your question to the central service.
2. The central service forwards the request to your Databricks workspace.
3. Genie processes the request and generates an answer in your workspace.
4. The answer returns to Microsoft Teams through the central service.

When you save a document as a PDF, the ap
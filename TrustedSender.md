# TrustedSender.md

**WHAT TrustedSender IS**  
TrustedSender is an automated decision-making process to “Decide whether to invite this person in.”
(https://www.yo-ai.ai/trust-and-transparency.html)

But, instead of making decisions about <em>the person</em>,<br/>
TrustedSender decides "whether to let this email in".

TrustedSender protects individuals and organizations from email compromise and phishing attacks,
and is designed to monitor compliance on a transactional level and calculate trust of participants in these communication channels. 
(https://www.yo-ai.ai/compliance.html)

I use my Yo-AI Assurance Platform to monitor all automated decisions made by my Yo-AI agents.
(https://www.yo-ai.ai/automated-decisions.html)

I also use a secure email gateway in front of the yo-ai.ai domain,
which my agents can access through the ToolRegistry.
(https://www.yo-ai.ai/tool-registry.html)


**HOW TrustedSender WORKS**  
A "Sender" is a unique email address used by an individual or organization to send email.
A "Recipient" decides "whether to let this email in".

In any exchange, you might be the "Sender" or you might be the "Recipient".  
It doesn't matter which side you are on or what role you play.  
Both sides have decisions to make:  
Do I send this email? Who should I send it to? Where should I send it?  
Who sent me this email? What is it about? Do I need to do something?

Go to <a href="https://www.privacyportfolio.com/trustedsender-registration.html">Trusted Sender Preferences</a>.

"This form gives you or your organization a simple, secure way to share the information my Yo‑AI agents need to interact with your automated processes."

The form itself can be used by humans manually,  
or by AI Agents using the
<a href="trustedsender-preferences-api.yaml">trustedsender-preferences-api.yaml</a>. 

This API wraps operations in other standalone modules and APIs for convenience and security,
so agents know their authorization scope before executing tasks.

This allows you to evaluate whether I am providing the same instructions to AI Agents that I also give to humans -- even if they use different methods to achieve the same goal.

If you weren't expecting to ALLOW AI AGENTS to interact with YOUR PROCESSES,
go to https://www.privacyportfolio.com/unsubscribe.html.

One Decision-Factor I use is: Can I reverse or undo my decision or action?  
I could sign up, select my preferences, try it once or twice, and unsubscribe to answer this question. 
(https://www.privacyportfolio.com/trustedsender-unsubscribe-form.html)

(A common theme embedded in Yo-AI's architectural philosophy is: bidirectional, and mutual processes.)


**WHAT I CAN DO WITH TrustedSender**  
I can migrate Senders from my three legacy email providers to my new email provider.  
I only want Senders that fit my own custom criteria but I'm also willing to help them honor my preferences.  
(TrustedSender_Decision_Factors.html is what I email to them.)

Without allowing ANY agents access to my legacy inboxes where they could use my credentials to impersonate me, I can export my legacy mailbox archives:

(imap_to_mbox.py) Exports email from a Comcast IMAP server to an mbox format. 

(eml_dir_to_mbox.py) Converts a directory of individual .eml files (as produced by Proton's
official proton-mail-export-cli tool) into a single mbox file, so
mbox_sender_analysis.py can be run against it unchanged.

(mbox_sender_analysis.py) Parses exported mbox files (Gmail Takeout, ProtonMail export, etc.) and
builds a per-sender decision-factors comma-delimited report, for use BEFORE sending
ChangeOfAddress notifications during domain migration — i.e. the
"Move & Lose" gate: senders who don't clear the bar don't get notified
of your new address.

(sender_org_inference.py) Given a sender_report.csv (from mbox_sender_analysis.py), produces a
suggested organization name and an "is this domain the actual
organization, or just an intermediary/ESP relaying on their behalf"
guess for each sender — meant to speed up the manual review you were
already doing, not replace it. Every row is a SUGGESTION with a
confidence flag, not a final answer.

(Comcast_Sender_Report.xlsx)  Formatted sender_report.csv for Comcast (example). 
Contains the following columns:
address	domain
message_count
first_seen
last_seen
auth_spf_verdicts_seen
auth_dkim_verdicts_seen
auth_dmarc_verdicts_seen
reply_to_mismatch_count
precedence_bulk_count
list_unsubscribe_present_count
noreply_address_count
user_ever_sent_to_this_address
migration_candidate_bucket

The total sum of MessageCount is 41,730 messages.  
The total sum of unique Senders is 4,331.  
Generally, the more email I get from Senders, the less important it is to me.

The total sum of last_seen greater than 2 years is 3,765.  
Obviously I probably don't want to invite Senders I haven't received messages from lately.

Then there are the Senders who DON'T HAVE unsubscribe links in their emails:  
The total sum of Senders whose list_unsubscribe_present_count=0 is 2,421.

Finally, there are Senders who DON'T WANT TO TALK TO ME. That's what I say when 
noreply_address_count = 100% of a Sender's email messages.

Those are the most useful Decision-Factors used to generate a streamlined "Invitation List".
Others I use are:  
reply_to_mismatch_count which indicates IMPERSONATION (authorized AND unauthorized)
and
145 suspected personal emails from 6 domains: gmail.com, outlook.com, yahoo.com, icloud.com, hotmail.com, protonmail.com.

As for all remaining Senders who ARE FILTERED OUT, they are STILL IN MY ARCHIVES.  
My agents that need to query the archives, can still do so, provided they have access permissions to them.


**Inviting TrustedSenders**  
I use email send templates I publish in the Paubox Email API to send email programmatically.  
/Migration/ChangeOfAddress_template.html is a Change of Address Notification Template sent from legacy email providers.  
These are SENT FROM my legacy mailboxes, which the Senders EXPECT. (They can identify me by my email address they have on record.)  
I do CC: craig-erickson@yo-ai.ai so I know which Senders I invited.

Then I wait to see who responds.  
Sometimes Senders reply directly to my invitation email at my legacy email address, my new address, or both.  
Often, Senders just change my email address (at the source -- wherever it is stored),   
and continue sending me promotional emails, even from subscriptions I never consented to receive.  
Rarely, will a Sender (or its agents) use the TrustedSender Registration form.

"I invited you to change my address. I did not invite you to fill out a form or promise me ANYTHING."


**Evaluating TrustedSenders**  
Any Sender that IS REGISTERED as a TrustedSender IS ALSO REQUIRED to maintain an alternative contact
for <em>adminstrative use</em>: an accountable human that is available to recieve notifications
or any other information about its communications associated with an individual or organization.

Any Sender that is NOT REGISTERED as a TrustedSender IS A GUEST of the individual or organization that invited them. In other words, an UNREGISTERED Sender's alternative contact is BY DEFAULT,
the TrustedSender that invited them. (Only TrustedSenders can invite other Senders.)

TrustedSenders are tagged [TrustedSender] in all incoming emails to yo-ai.ai, which is prepended to the Subject line automatically by my Paubox Email Gateway.  
This speeds up processing by reducing friction, but every email is still evaluated EVEN FOR TrustedSenders,  
which are assigned "trust-levels" that increment or decrement a number greater or less than zero.  
(View my <a href="">Door-Keeper Extended Agent Card</a>.)

trustedsender_request_response_template.html is used to automatically respond to UntrustedSenders from yo-ai.ai. The opening paragraph reads:

<p>
Your message isn't singled out. Everything sent to this inbox is quarantined by default — deny-all, no exceptions.<br/>
When we recieve messages from individuals or organizations at this email domain,<br/>
the following controls are used to assign a trust levels to each unique address used<br/>
to send me email from your organization: {{CTP_org_name}}
</p>

This template is in my Paubox Email API Template Library. 
I send it to every UntrustedSender discovered in my inbox whether they were invited OR NOT.
The primary control the first paragraph refers to is the Paubox "Inbound Security" feature,
which natively quarantines email without the required encryption protocols, sensitive personal information in its content, or other customized Data Loss Prevention (DLP) rules.

I quarantine EVERY EMAIL BY DEFAULT, AFTER ALLOWING white-listed TrustedSenders IN.  
Paubox sends Quarantine Reports and DLP Notifications to my administrative email address at
craig-erickson@privacyportfolio.com, which is NOT secured by Paubox.  
These emails are used to trigger a lambda function that:  
parses the emails for quarantined messages,  
looks up the message-id,  
retrieves the email from quarantine,  
saves the original email and header,  
appends it to the Yo-AI platform log,  
and sends it back to Yo-AI as a forwarded message from craig-erickson@privacyportfolio.com,  
which bypasses my default quarantine rule because I am registered as a TrustedSender.

The next step (before sending the trustedsender_request_response) 
is letting my Yo-AI agents analyze each downloaded email message.

Because I want to CULTIVATE TrustedSenders,  
I share my analysis with them so they have the opportunity to decide what they want to do.

The title of (SenderEmailAnalysis.html) reads:  
<strong>What your email tells me about you as a Sender</strong>

SenderEmailAnalysis.html contains "findings":   
some of them are facts,  
a few of them may be actual test results,  
but many of them are inferences made by AI,  
and some are human interpretations - often influenced by emotional responses.

Just to recap this section,  
a Sender email inbound to yo-ai.ai is quarantined and analyzed,  
but INSTEAD OF directly replying from inside my 'live inbox',  
I send an out-of-band response from the Paubox Email API  
so I can track opens, blocks, reads, etc.  
And so can my agents.

No decision is made at this point about whether to ALLOW, BLOCK, or CULTIVATE the Sender.


**Cultivating TrustedSenders**  
Trust isn't given -- it's earned.  
I need to continuously earn the trust of my TrustedSenders,  
based on my last email to them -- the one they're likely to remember!

Those who registered as TrustedSenders are provided with instructions and tools to conduct their own assessment of me and my agents.  
Perhaps the Decision-Factors I used to make a Decision-Outcome are inaccurate.  
Or maybe I made a mistake -- and sent the wrong information to the wrong person!

<pre>
<p>
<span>From:&nbsp;&nbsp;{{CP_sender_email_display_name}} at {{CP_sender_email}}</span><br/> 
<span>Location:&nbsp;{{CP_location}}</span><br/> 
<span>Date:&nbsp;&nbsp;{{M_sent_date}}</span>
<span>To:&nbsp;&nbsp;&nbsp;{{CTP_sender_email}}</span> 
<span>Subject:&nbsp;What my email tells you about me as a Sender</span>
</p>
</pre>

I use a Template_Placeholder_DataDictionary.md for:  
 Paubox Email API Templates  
 Paubox Marketing API Templates  
 Paubox Forms  
This helps me keep subscriber information secure and accurate.

Too many placeholders can also be an issue:  
<div>
    <h3>{{CP_OBO}}'s lab results are ready</h3>
{{M_message_content}}
</div>  
This solution uses only two placeholders.

TrustedSenders are subscribers who consented to entrust me and my agents with their data.  
They are identifiable by mapping the 
<meta name="x-recipient-id" content="{{CTP_sender_id}}"> in the email header  
to the subscriber_uuid in Paubox  
to minimize exposing personally-identifiable information in the templates,  
in the Paubox platform,  
or in your Contacts -- the first place where hackers and AI Agents look.

This mapping is confidential, secure, and subject to change in real-time!

Managing subscriptions and subscribers is the second level of the TrustedSender Program.  
The first level is email security.


**Protecting TrustedSenders**  
TrustedSenders can subscribe to filtered kafka topics of events from the Yo-AI Platform log,  
so they can see all communication activity on MY SIDE,  
and compare with logs ON THEIR SIDE to ESTABLISH FACTS.

TrustedSenders can configure their communication preferences,  
to receive CONSOLIDATED REPORTS on ALL Senders associated with an Organization or Individual.

TrustedSenders can ALSO configure their communication preferences,  
to include voice and SMS text messages, chats, videos, and meetings.

I use RingCentral for these other communication channels, which generates and sends email summaries
to my inbox at yo-ai.ai where it is processed through the Paubox email gateway like any other email message:
saved, logged, and analyzed.

Paubox also handles attachments, applying its native security capabilities to determine if they are malformed, malicious, or contains sensitive personal information.

TrustedSenders can configure their communication preferences UNIVERSALLY -- meaning they can unsubscribe TO ALL COMMUNICATION CHANNELS.


**Building Your Own TrustedSender Program**  
I built my TrustedSender Program using MY preferred tools.  
While there's nothing stopping you from running your own Yo-AI Assurance Platform, Paubox Email Gateway, RingCentral tenant, or AWS cloud environment -- you SHOULD be able to implement a TrustedSender Program with the TOOLS YOU PREFER.  
(I haven't tried it yet, but I'm available to assist you.)  
 

**Promoting Your TrustedSender Program**  
The Yo-AI Assurance Platform is designed to run <a href="https://www.privacyportfolio.com/campaigns.html">Campaigns</a>.  
The TrustedSender Campaign is an outreach to influence Senders to participate in or host a TrustedSender Program.  
In this case, the "conversion rate" is the ratio of Senders who become TrustedSenders.

**Leveraging Your TrustedSender Program**  
TrustedSender can be used to:
- establish first-party relationships (ControllingParty) with third-party processors (IntermediaryParty).
- discover which Organizations or Individuals a Sender is acting On-Behalf-Of (OBO).
- detect changes in ownership, branding, infrastructure, vendors.
- provide evidence you are NOT VIOLATING any agreements or policies with the Sender.

**WHAT YOU CAN DO WITH TrustedSender**  
If you DON'T have Paubox:  
    Request a QR code to get $250 discount on a subscription plan.
    Request assistance for integrating the TrustedSender Program with other email gateway solutions.
If you DON'T have RingCentral:  
    Request a QR code to get a $300 discount on a subscription plan.  
    Request assistance for integrating the TrustedSender Program with other telecommunications solutions
    such as Twilio Voice, SMS, or Chat.
If you DON'T have Yo-AI:  
    Clone, modify, and host the Yo-AI Assurance Platform in your environment.  
    Request assistance for integrating the TrustedSender Program with other AI Agent platforms.
If you DON'T have AWS:
    Replace or refactor lambda functions with similar serverless functions or cloud APIs suited for your environment. Do it yourself or request assistance if needed.

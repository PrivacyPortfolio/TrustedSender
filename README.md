# TrustedSender Repository File Structure
```
/TrustedSender
    README.md
        - TrustedSender Repository File Structure
    TrustedSender.md
        - Explainer document
    /artifacts
        /forms
            GeneralUnsubscribe_paubox_form.html
            trustedsender-unsubscribe-form.html
                - where trustedsenders are directed from the unsubscribe page
                - AI Agents of trustedsenders are directed to use the trustedsender-preferences-api.yaml
                  (UniversalUnsubscribe)
            TrustedSender_Registration_paubox_form.html
            UniversalUnsubscribe_paubox_form.html
        /landing_pages
            trusted-sender.html
                - Landing page for Senders who want to learn more about registering as a TrustedSender.
                -> Senders who receive a link to the Secure Notification Center AND click on the
                PrivacyPortfolio logo lands here:
                https://www.yo-ai.ai/trusted-sender.html
                This page assumes the Sender is Untrusted, and sends no-reply emails to PrivacyPortfolio, Yo-ai, or Craig Erickson with or without my consent.
            trustedsender-registration.html
                - aka "Trusted Sender Preferences"
                -> related to trustedsender-preferences-api.yaml
                -> Static webpage that explains the TrustedSender Program and registers them via a Paubox form if desired
            unsubscribe.html 
		- website footer link serving a static page explaining unsubscribe options for ANYONE.
	/subscription
		Template_Placeholder_DataDictionary.md
                - This data dictionary maintains placeholders for Paubox Dynamic Email Templates
	/templates
		TrustedSender_Decision-Factors_Template.html 
			- explains how automated decisions are made about Senders.
		External_Counsel_Notification_template.html
			- sent by proxy to external law firms when Organizations block or ignore communications 	
		trustedsender_request_response_template.html
			- sent to UnTrustedSenders at yo-ai.ai 
		sender_email_analysis_template.html
			- transparent disclosure of why a message was quarantined, triggered on quarantine, via Lambda
		CCPA_LIMIT_Request_Template.html
			- sent to Intermediary Parties when First-Party blocks or ignores communications
		Clinical_Lab_Results_template.html
			- sent to medical providers when a new event is generated for a patient.
			<h3>{{CP_OBO}}'s lab results are ready</h3> or 
			<h3>Re: {{CP_OBO}}'s scheduled appointment</h3>
    /code
    	/EmailAnalysis
                mbox_sender_analysis.py
                  - Parses exported mbox files and builds a sender_report.csv,
			  	  used as decision-factors for sending ChangeOfAddress notifications.
                sender_org_inference.py
				  - Uses a sender_report.csv from mbox_sender_analysis.py to produce a
			  	  suggested organization name and an "is this domain the actual
			  	  organization, or just an intermediary/ESP relaying on their behalf"
			  	  guess for each sender. Every row is a SUGGESTION with a
			  	  confidence flag, not a final answer.
                WorkMailForwarder_lambda.py
				  - Pulls the raw MIME message from WorkMail
				  - Parses subject, sender, and body
				  - Sends a new email through Paubox to the solicitor-general
				  - Preserves HTML formatting
				  - Works with encrypted inbound mail (Paubox handles encryption on send)
    	/MailboxMigration
			eml_dir_to_mbox.py
				- Converts a directory of individual .eml files into a single mbox file
			imap_to_mbox.py
				- Cross-platform (Windows/Mac/Linux) IMAP export to mbox
    	/Paubox
    		/EmailAPI
			add_attachments.py
			download_attachment.py
			get_email_disposition.py
			get_email_template.py
			get_received_email.py
   			list_email_attachments.py
   			list_received_emails.py
   			list_receiving_domains.py
   			send_email_message.py
   			send_templated_email.py
			update_email_template.py
			/FormsAPI
				export_submissions_as_csv.py
				export_submission_as_csv.py
				export_submission_as_pdf.py
				get_form submissions.py
				get_forms.py
				get_form_definition.py
				get_form_metadata.py
				get_form_statistics.py
				get_submission_signature_image.py
				submit_form_response.py
				update_form.py
			/MarketingAPI
                create_subscriber.py
                create_subscription.py
                create_subscription_list.py
                get_campaign mailings.py
                get_campaign_analytics.py
                get_campaign_deliveries.py
                get_campaign_mailing.py
                get_campaign_sends.py
                get_subscriber.py
                get_subscribers.py
                get_subscribers_by_tracking_link.py
                get_subscription.py
                get_subscriptions.py
                get_subscription_lists.py
                get_tracking_links.py
                get_tracking_link_interactions.py
                send_campaign_mailings.py
                unsubscribe_subscribers.py
                unsubscribe_subscription.py
                update_subscriber.py
		/RingCentral
			delete_call_log.py
   			get_call_logs.py
   			update_message_store_configuration.py
			/AI
				analyze_sentiment.py
     			detect_intent.py
     			extract_topics.py
      			keyword_spotting.py
      			transcribe_call.py
			/SMS
      			delete_sms_message.py
      			get_sms_messages.py
     			send_sms_message.py
      			subscribe_sms_events.py
      			unsubscribe_sms_events.py
			/Voice
          		place_voice_call.py
        		update_caller_blocking.py
		/TrustedSenderPreferences
			trustedsender_preferences_api.yaml
				- my API that wraps: 
				  Paubox Marketing API, Paubox Email API, Paubox Forms API, RingCentral API, Yo-API.
			/AccessControls
				tool_registry.py  (data_steward_tool_registry.py used as stub example)
					- which tools and configurations agents can use
			/Monitoring
			/Registration
				unsubscribe_lambda.py
				- TrustedSender action Lambda for API Gateway routes.
	/config
		paubox.env.txt (stub)
	/private
		<!-- real content NOT PUBLIC -->
		PrivacyPortfolio
			tree-files.txt 
				- used as metadata for representing sensitive content that doesn't belong in a public repo.
```

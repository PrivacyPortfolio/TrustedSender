Template_Placeholder_DataDictionary.md

This data dictionary maintains placeholders for:
 Paubox Email API Templates
 Paubox Marketing API Templates
 Paubox Forms

Its purpose is to ensure the wrong content is never sent to the wrong subscriber.

Summary Table (Role Breakdown)	

{{placeholder}}	                                    Usage
---------------                                     -----
CP (Controlling Party — You)                        Role	
    {{CP_sender_email}}                                 Mailbox Sent From
    {{CP_sender_email_display_name}}                    Display Name Sent From
    {{CP_caller_phone}}                                 Phone Number Called From	
    {{CP_caller_phone_display_name}}	                Phone Display Name Called From
    {{CP_contact_email}}                                Mailbox to Contact
    {{CP_contact_email_display_name}}                   Display Name to Contact
    {{CP_contact_phone}}	                            Phone Number to Contact
    {{CP_contact_phone_display_name}}	                Phone Display Name to Contact
    {{CP_sender_prior_email}}                           Prior Mailbox Sent From
    {{CP_sender_prior_email_display_name}}              Prior Display Name Sent From
    {{CP_caller_prior_phone}}	                        Prior Phone Number to Contact
    {{CP_caller_prior_phone_display_name}}	            Prior Phone Display Name to Contact
    {{CP_location}}	                                    Street Address, City, State, Postal code, Country
    {{CP_domain}}                                       TLD Affiliated With, or Registered To
    {{CP_org_name}}                                     {{CP_OBO}} (if no org)
    {{CP_OBO}}  	                                    Person or Organization Represented 
    {{CP_type}} 	                                    Role, Relation
    {{CP_trusted_sender_tag}}                           Identifier Tag 
    {{CP_channel_preferences}}                          Email, Voice, SMS, Social, USPS, API	
    {{CP_campaign_preferences}}	                        Notify, Report
    {{CP_decision_factor_reciprocity}}                  true|false
    {{CP_decision_factor_friction}}                     true|false
    {{CP_decision_factor_dpa}}	                        true|false
    {{CP_relation}}	                                    Consumer, Customer, Sponsor, Regulator, Investor, Processor, Representative, Researcher, Provider

    
CTP (Counter Party — Them)	                        Role
    {{CTP_sender_email}}                                 Mailbox Sent From
    {{CTP_sender_email_display_name}}                    Display Name Sent From
    {{CTP_caller_phone}}                                 Phone Number Called From	
    {{CTP_caller_phone_display_name}}	                 Phone Display Name Called From
    {{CTP_contact_email}}                                Contact Mailbox
    {{CTP_contact_email_display_name}}                   Contact Display Name
    {{CTP_contact_phone}}	                             Phone Number to Contact
    {{CTP_contact_phone_display_name}}	                 Phone Display Name to Contact
    {{CTP_sender_prior_email}}                           Prior Mailbox
    {{CTP_sender_prior_email_display_name}}              Prior Display Name
    {{CTP_caller_prior_phone}}	                         Prior Phone Number to Contact
    {{CTP_caller_prior_phone_display_name}}	             Prior Phone Display Name to Contact
    {{CTP_location}}	                                 Street Address, City, State, Postal code, Country
    {{CTP_domain}}                                       TLD Affiliated With, or Registered To
    {{CTP_org_name}}                                     {{CTP_OBO}} (if no org)
    {{CTP_OBO}}  	                                     Person or Organization Represented 
    {{CTP_type}} 	                                     Person|Organization
    {{CTP_trusted_sender_tag}}                           Identifier Tag 
    {{CTP_channel_preferences}}                          Email, Voice, SMS, Social, USPS, API	
    {{CTP_campaign_preferences}}                         Notify, Report
    {{CTP_decision_factor_reciprocity}}                  true|false
    {{CTP_decision_factor_friction}}                     true|false
    {{CTP_decision_factor_dpa}}	                         true|false
    {{CTP_relation}}	                                 Consumer, Customer, Sponsor, Regulator, Investor, Processor, Representative, Researcher, Provider
    
IP (Intermediary Party — Via)	                    Role
    {{IP_sender_email}}                                 Mailbox Sent From
    {{IP_sender_email_display_name}}                    Display Name Sent From
    {{IP_caller_phone}}                                 Phone Number Called From	
    {{IP_caller_phone_display_name}}	                Phone Display Name Called From
    {{IP_contact_email}}                                Contact Mailbox
    {{IP_contact_email_display_name}}                   Contact Display Name
    {{IP_contact_phone}}	                            Phone Number to Contact
    {{IP_contact_phone_display_name}}	                Phone Display Name to Contact
    {{IP_sender_prior_email}}                           Prior Mailbox
    {{IP_sender_prior_email_display_name}}              Prior Display Name
    {{IP_caller_prior_phone}}	                        Prior Phone Number to Contact
    {{IP_caller_prior_phone_display_name}}	            Prior Phone Display Name to Contact
    {{IP_location}}	                                    Street Address, City, State, Postal code, Country
    {{IP_domain}}                                       TLD Affiliated With, or Registered To
    {{IP_org_name}}                                     {{IP_OBO}} (if no org)
    {{IP_OBO}}  	                                    Person or Organization Represented 
    {{IP_type}} 	                                    Person|Organization
    {{IP_trusted_sender_tag}}                           Identifier Tag 
    {{IP_channel_preferences}}                          Email, Voice, SMS, Social, USPS, API	
    {{IP_campaign_preferences}}                         Notify, Report
    {{IP_decision_factor_reciprocity}}                  true|false
    {{IP_decision_factor_friction}}                     true|false
    {{IP_decision_factor_dpa}}	                        true|false
    {{IP_relation}}	                                    Consumer, Customer, Sponsor, Regulator, Investor, Processor, Representative, Researcher, Provider

    
SP (Stakeholder Party — referenced entities)        Role	
    {{SP_sender_email}}                                 Mailbox Sent From
    {{SP_sender_email_display_name}}                    Display Name Sent From
    {{SP_caller_phone}}                                 Phone Number Called From	
    {{SP_caller_phone_display_name}}	                Phone Display Name Called From
    {{SP_contact_email}}                                Contact Mailbox
    {{SP_contact_email_display_name}}                   Contact Display Name
    {{SP_contact_phone}}	                            Phone Number to Contact
    {{SP_contact_phone_display_name}}	                Phone Display Name to Contact
    {{SP_sender_prior_email}}                           Prior Mailbox
    {{SP_sender_prior_email_display_name}}              Prior Display Name
    {{SP_caller_prior_phone}}	                        Prior Phone Number to Contact
    {{SP_caller_prior_phone_display_name}}	            Prior Phone Display Name to Contact
    {{SP_location}}	                                    Street Address, City, State, Postal code, Country
    {{SP_domain}}                                       TLD Affiliated With, or Registered To
    {{SP_org_name}}                                     {{IP_OBO}} (if no org)
    {{SP_OBO}}  	                                    Person or Organization Represented 
    {{SP_type}} 	                                    Person|Organization
    {{SP_trusted_sender_tag}}                           Identifier Tag 
    {{SP_channel_preferences}}                          Email, Voice, SMS, Social, USPS, API	
    {{SP_campaign_preferences}}                         Notify, Report
    {{SP_decision_factor_reciprocity}}                  true|false
    {{SP_decision_factor_friction}}                     true|false
    {{SP_decision_factor_dpa}}	                        true|false
    {{SP_relation}}	                                    Consumer, Customer, Sponsor, Regulator, Investor, Processor, Representative, Researcher, Provider
    
M (Message Metadata)                                Message Object	
    {{M_message_uuid}}                                  Message-ID	
    {{M_message_type}}	                                Template-ID
    {{M_sent_date}}	                                    Date Sent
    {{M_event_date}}	                                Date Referenced
    {{M_message_content}}	                            HTML Content Snippet
    
R (Resources)	                                    Resource Object
    {{R_resource_uuid}}                                 Identifier	
    {{R_resource_type}}	                                Data|Tool|Service|Product
    {{R_resource_label}}	                            Governance Tag
    {{R_resource_url}}	                                Location
    {{R_resource_owner}}	                            Person|Organization
    {{R_resource_consumer}}	                            Person|Organization

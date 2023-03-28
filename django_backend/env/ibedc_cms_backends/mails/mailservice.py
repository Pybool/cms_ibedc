from django.core.mail import send_mail, EmailMultiAlternatives
import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

                            
class Mailservice(object):

        
    def crmd_approval_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>Your Customer Record Modification submission has been approved by {2}</p>
                </div>
                """
                
    def caad_approval_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>You have a  Customer Account Adjustment submission task awaiting your review and approval {2}</p>
                </div>
                """
                
    def caad_initiate_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>Please conduct a second level validation at the premises of the customer in this mail</p>
                        {2}
                </div>
                """
                
    def caad_validate_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>The CAAD record below awaits your validation</p>
                        {2}
                </div>
                """
         
    def send_outwards_mail(mail_parameters):
        
        try:
            templates = {"crmd_approval":Mailservice.crmd_approval_template,
                         "caad_approval":Mailservice.caad_approval_template,
                         "caad_initiate":Mailservice.caad_initiate_template,
                         "caad_validate":Mailservice.caad_validate_template}
            html_content = templates[mail_parameters['ir_template']]()
            html_content = html_content.format(mail_parameters['subject'],mail_parameters['recipients'][0],str(mail_parameters.get('body')))
            print("HTMLS ====> ",html_content)
            
            msg = EmailMultiAlternatives(mail_parameters['subject'],"",mail_parameters['sender'], mail_parameters['recipients'])
            msg.attach_alternative(html_content, "text/html")
            mail_status = msg.send() 
            return mail_status
            
        except Exception as e:
            print(str(e))
        
    
       
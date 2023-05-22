from django.core.mail import send_mail, EmailMultiAlternatives
import os
from .templates import initiatecaad
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

base_url = 'http://192.168.15.161:4200'
                            
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
        # return """  
        #         <div class="col-12">
        #             <h2 style="color:blue;">{0}</h2>
        #             <h4>Dear {1}</h4>,
        #                 <p>Please conduct a second level validation at the premises of the customer in this mail</p>
        #                 {2}
        #         </div>
        #         """
        print(initiatecaad.template)
        return initiatecaad.template
                
    def caad_validate_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>The CAAD record below awaits your validation</p>
                        {2}
                </div>
                """
                
    def caad_creation_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>The CAAD record below was created</p>
                        {2}
                </div>
                """
                
    def crmd_creation_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>The crmd record below was created</p>
                        {2}
                </div>
                """
                
    def crmd_update_template():
        return """  
                <div class="col-12">
                    <h2 style="color:blue;">{0}</h2>
                    <h4>Dear {1}</h4>,
                        <p>The crmd record below was updated</p>
                        {2}
                </div>
                """
         
    def send_outwards_mail(mail_parameters):
        
        try:
            templates = {"crmd_approval":Mailservice.crmd_approval_template,
                         "caad_approval":Mailservice.caad_approval_template,
                         "caad_initiate":Mailservice.caad_initiate_template,
                         "caad_validate":Mailservice.caad_validate_template,
                         "crmd_creation":Mailservice.crmd_creation_template,
                         "crmd_update":Mailservice.crmd_update_template}
            html_content = templates[mail_parameters['ir_template']]()
            databody =  mail_parameters.get('body')
            html_content = html_content.format(
                                                mail_parameters['subject'],
                                                mail_parameters['recipients'][0],
                                                databody.get('firstname'),
                                                databody.get('surname'),
                                                databody.get('othernames'),
                                                databody.get('mobile'),
                                                databody.get('accountno'),
                                                databody.get('meterno'),
                                                databody.get('address') or databody.get('address1'),
                                                databody.get('state'),
                                                databody.get('buid'),
                                                databody.get('servicecenter'),
                                                databody.get('dss_id'),
                                                databody.get('accounttype'),
                                                base_url
                                                )
            print("HTMLS ====> "+html_content+initiatecaad.css)
            
            msg = EmailMultiAlternatives(mail_parameters['subject'],"",'no-reply-cms@ibedc.com', mail_parameters['recipients'])
            msg.attach_alternative(html_content+initiatecaad.css, "text/html")
            mail_status = msg.send() 
            return mail_status
            
        except Exception as e:
            print("===>",str(e))
        
    
       
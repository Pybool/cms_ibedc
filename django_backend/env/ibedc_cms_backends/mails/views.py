
from rest_framework.views import APIView
from rest_framework.response import Response
from tasks.__task__email import *
from mails.mailservice import Mailservice
import logging

class Test(APIView):
    
    def get(self,request):
        mail = {"ir_template":"crmd_approval",
                "url":"",
                "subject":"Customer Account Adjustment Document Approval",
                "sender":'noreply@ibedc.com', 
                "recipients":['devops@hq.com']}
        send_outward_mail.delay(mail)
        print("---------------",mail)
        return Response(mail)
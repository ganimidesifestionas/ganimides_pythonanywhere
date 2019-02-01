# email_services/email_services.py
#import sys
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mailjet_rest import Client

from .. import app

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
#import sendgrid
#from sendgrid.helpers.mail import *

def send_email(parTo,parSubject,parContentHtml,parContentText='',parContentTemplate=''):
    """
    send_email (wrapper)
    """
    print('@@@^^^@@@ send_email','start')

    appFrom=app.config['MAIL_SENDER']
    print('   from:',appFrom)

    if not(appFrom):
        app.logger.info('   %s No mail sender', 'send_email')
        return('No Mail sender defined')

    if not(parTo):
        app.logger.info('   %s No Recipient', 'send_email')
        return('No Recipient')
    if not(parSubject):
        app.logger.info('   %s No Subject', 'send_email')
        return('No Subject')
    if not(parContentHtml) and not(parContentText) and not(parContentTemplate):
        app.logger.info('   %s No Content', 'send_email')
        return('No Content')

    print('    MAIL provider=',app.config['MAIL_SERVER_PROVIDER'])
    print('    MAIL server=',app.config['MAIL_SERVER'])
    print('    MAIL port=',app.config['MAIL_PORT'])
    print('    MAIL tls=',app.config['MAIL_USE_TLS'])
    print('    MAIL ssl=',app.config['MAIL_USE_SSL'])
    print('    MAIL username=',app.config['MAIL_USERNAME'])
    print('    MAIL password=',app.config['MAIL_PASSWORD'])
    print('    MAIL apikey_public=',app.config['MAIL_APIKEY_PUBLIC'])
    print('    MAIL apikey_private=',app.config['MAIL_APIKEY_PRIVATE'])

    try:
        #result=sendEmail_using_SMTP(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
        #result=sendEmail_thru_mailjet_api(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
        if app.config['MAIL_SERVER_PROVIDER']=='mailjet':
            if app.config['MAIL_SEND_METHOD']=='SMTP':
                result=sendEmail_using_SMTP(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
            else:
                result=sendEmail_thru_mailjet(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
        else:
            if app.config['MAIL_SERVER_PROVIDER']=='yandex':
                if app.config['MAIL_SEND_METHOD']=='SMTP':
                    result=sendEmail_using_SMTP(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
                else:
                    result=sendEmail_thru_sendgrid(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
            else:
                result=sendEmail_using_SMTP(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
                #result=sendEmail_thru_google(appFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
    except Exception as error_text:
        result=error_text

    print('@@@^^^@@@ send_email result:',result)
    return(result)

def sendEmail_using_SMTP(parFrom,parTo,parSubject,parContentHtml,parContentText='',parContentTemplate=''):
    """
    sendEmail_using_SMTP
    """
    try:
        msg=FormattedEmailMessage(parFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
        if not(msg):
            app.logger.info('      %s can not format email message', 'sendEmail_thru_google')
            return 'can not format email message'
    except Exception as error_text:
        app.logger.info('      %s exception:%s', 'sendEmail_thru_google',error_text)
        return error_text

    try:
        print('   sendEmail_using_SMTP start------------------------------------')
        mail = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        mail.ehlo()
        mail.starttls()
        mail.login(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        #mail.login('scantzochoiros@gmail.com','philea13')
        mail.sendmail(parFrom, parTo, msg.as_string())
        mail.quit()
        print('   sendEmail_using_SMTP finish-----------------------------------')
    except Exception as error_text:
        print('   sendEmail_using_SMTP ERROR:',error_text)
        return error_text

    return 'OK'



def sendEmail_thru_google(parFrom,parTo,parSubject,parContentHtml,parContentText='',parContentTemplate=''):
    """
    sendEmail_thru_google
    """
    try:
        msg=FormattedEmailMessage(parFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
        if not(msg):
            app.logger.info('      %s can not format email message', 'sendEmail_thru_google')
            return 'can not format email message'
    except Exception as error_text:
        app.logger.info('      %s exception:%s', 'sendEmail_thru_google',error_text)
        return error_text

    try:
        print('@@@^^^@@@ sendEmail_thru_google start------------------------------------')
        mail = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        mail.ehlo()
        mail.starttls()
        #mail.login('bstarr131@gmail.com', 'bstarr13')
        #mail.login('scantzochoiros@gmail.com', 'philea13')
        mail.login(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        mail.sendmail(parFrom, parTo, msg.as_string())
        mail.quit()
        print('@@@^^^@@@ sendEmail_thru_google finish-----------------------------------')
    except Exception as error_text:
        print('@@@^^^@@@ sendEmail_thru_google ERROR:',error_text)
        return error_text

    return 'OK'

def sendEmail_thru_mailjet(parFrom,parTo,parSubject,parContentHtml,parContentText='',parContentTemplate=''):
    """
    sendEmail_thru_mailjet
    """
    try:
        msg=FormattedEmailMessage(parFrom,parTo,parSubject,parContentHtml,parContentText,parContentTemplate)
        if not(msg):
            app.logger.info('      %s can not format email message', 'sendEmail_thru_google')
            return 'can not format email message'
    except Exception as error_text:
        app.logger.info('      %s exception:%s', 'sendEmail_thru_google',error_text)
        return error_text

    try:
        print('   sendEmail_thru_mailjet start------------------------------------')
        mail = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        mail.ehlo()
        mail.starttls()
        mail.login(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        mail.sendmail(parFrom, parTo, msg.as_string())
        mail.quit()
        print('   sendEmail_thru_mailjet finish-----------------------------------')
    except Exception as error_text:
        print('   sendEmail_thru_mailjet ERROR:',error_text)
        return error_text

    return 'OK'

def sendEmail_thru_sendgrid(parFrom,parTo,parSubject,parContentHtml,parContentText='',parContentTemplate=''):
    """
    sendEmail_thru_sendgrid
    """
    try:
        #echo "export SENDGRID_API_KEY='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'" > sendgrid.env
        #echo "sendgrid.env" >> .gitignore
        #source ./sendgrid.env
        #SENDGRID_API_KEY='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'
        #sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        #parFrom="noreply@ganimides.com"
        #from_email = Email(parFrom)
        #to_email = Email(parTo)
        #subject = parSubject
        #content = Content("text/plain", "and easy to do anywhere, even with Python")
        #mail = Mail(from_email, subject, to_email, content)
        #response = sg.client.mail.send.post(request_body=mail.get())
        # print('response.status_code=', response.status_code)
        # print('response.body=', response.body)
        # print('response.headers=', response.headers)
        return 'OK'
    except Exception as error_text:
        print('   sendEmail_thru_sendgrid ERROR:',error_text)
        return error_text

def sendEmail_thru_mailjet_api(parFrom,parTo,parSubject,parContentHtml,parContentText='',parContentTemplate=''):
    """
    sendEmail_thru_mailjet_api
    """
    api_key = os.environ['MAIL_APIKEY_PUBLIC']
    api_secret = os.environ['MAIL_APIKEY_PRIVATE']

    try:
        #mailjet = Client(auth=(api_key, api_secret), version='v1.3.0')
        mailjet = Client(auth=(api_key, api_secret))
        print('   sendEmail_thru_mailjet_api CONNECT OK')
    except Exception as error_text:
        print('   sendEmail_thru_mailjet_api ERROR api authorization failed:',error_text)
        return error_text

    data1 = {
        'FromEmail': 'your sender email'
        ,'Subject': 'Hello Mailjet!'
        ,'Text-Part': 'Welcome Onboard'
        ,'Recipients': [{'Email': 'recipient email'}]
    }

    data = {
          'Messages': [
        	{
        		"From": {
        			"Email": parFrom,
        			"Name": "Mailjet Pilot"
        		},
        		"To": [
        			{
        			"Email": parTo,
        			"Name": "passenger"
        			}
        		],
        		"Subject": parSubject,
        		"TemplateLanguage": True,
        		"TextPart": "Dear {{data:firstname:\"passenger\"}}, welcome to Mailjet! ",
        		"HTMLPart": "Dear {{data:firstname:\"passenger\"}}, welcome to Mailjet!"
        	}
        ]
    }

    print('   sendEmail_thru_mailjet_api DATA=',data)

    try:
        result = mailjet.send.create(data=data)
        print ('   mailjet.send status_code:',result.status_code)
        print ('   mailjet.send json:',result.json())
        print ('   mailjet.send OK')
        return 'OK'
    except Exception as error_text:
        print('   sendEmail_thru_mailjet_api ERROR:',error_text)
        return error_text

def FormattedEmailMessage(parFrom,parTo,parSubject,parContentHtml,parContentText='',parContentTemplate=''):
    # Create message container - the correct MIME type is multipart/alternative.
    print('   @@@FormattedEmailMessage')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = parSubject
    msg['From'] = parFrom
    msg['To'] = parTo

    if parContentTemplate=='x':
        # Create the body of the message (a plain-text and an HTML version).
        parContentText = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        parContentHtml = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.

    # Record the MIME types of both parts - text/plain and text/html.
    if parContentText:
        part1 = MIMEText(parContentText, 'plain')
        msg.attach(part1)

    if parContentHtml:
        part2 = MIMEText(parContentHtml, 'html','utf8')
        msg.attach(part2)

    return msg
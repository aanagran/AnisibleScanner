import smtplib,logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from django.template import loader
from email import encoders
from django.conf import settings








def send_mail(to_email,username,csv_path,csv_file_name):
    try:
        TO_EMAIL = to_email
        args = {}
        args = {'username': username}
        
        loadTemplatepath='report_email_template.html'

        template=loader.get_template(loadTemplatepath)
        final_message = template.render(args)


        msg = MIMEMultipart('alternative')
        msg['Subject'] = settings.SUBJECT
        msg['From'] = settings.SMTP_EMAIL
        msg['To'] = TO_EMAIL


        html_part = MIMEText(final_message, 'html')
        msg.attach(html_part)
        # Attach the file
        attachment = open(csv_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(csv_file_name))
        msg.attach(part)
        mailserver = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        logging.info({'message:':'initiate smtp conn','mailserver':mailserver})
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mail_login = mailserver.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)

        mail_status = mailserver.sendmail(settings.SMTP_EMAIL, TO_EMAIL, msg.as_string())#sending an email
        logging.info({'mail_login':mail_login,'mail_status':mail_status})
        mailserver.quit()
        logging.info({'message:':'Mail sent','to_email:':TO_EMAIL})
    except Exception as err:
        logging.info({'Exception_in_mail_connection:': str(err)})



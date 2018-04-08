import smtplib
import logging
import socket

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

logger = logging.getLogger(__name__)

def send_email():

    from_address= "os.divine@fbk.eu"
    to_address = ["tefera@fbk.eu", "kindeg12@gmail.com"]
    multipart = MIMEMultipart()

    multipart['From'] = from_address
    multipart['To'] = ', '.join(to_address)
    multipart['Subject'] = "DiVINE Report"
    
    body = "Please check the attachment for the Divine cloud information. \n\nBest Regards,"
    multipart.attach(MIMEText(body, 'plain'))

    filename = "fileOutput.xlsx"
    base = MIMEBase('application', 'octet-stream')

    try:
        logger.info("Opening attachement file ...")
        with open(filename, "rb") as attachment:
            base.set_payload((attachment).read())

    except FileNotFoundError as e:
        logger.error("Error occured while opening the the file: {}\n{}".format(filename, e))
        raise

    encoders.encode_base64(base)
    base.add_header('Content-Disposition', 'attachment; filename = {0}'.format(filename))
    multipart.attach(base)
    e_message = multipart.as_string()

    try:
        logger.info("Sending email via smtp service ...") 
        server = smtplib.SMTP('grelay.fbk.eu', 25)
        server.starttls()
        server.sendmail(from_address, to_address, e_message)
        server.quit()
        
    except socket.gaierror as e:
        logger.error("Error occured while getting SMTP address name or service {0}".format(e))
        raise
        
    except smtplib.SMTPRecipientsRefused as e:
        logger.error("Error occured while sending email to the recipient address {0}".format(e))
        raise






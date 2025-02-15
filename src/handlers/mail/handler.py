"""A handler that sends mails."""

import smtplib
import os.path
from ConfigParser import RawConfigParser

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
SENDER_MAIL = CONFIG.get('mail', 'sender')
SMTP_SERVER = CONFIG.get('mail', 'smtp_server')


class MailHandler():
    """Handler is initialized with two functions, the first being a
    predicate to decide whether to send a mail, the second returning
    a list of recipient mail addresses."""
    
    def __init__(self, interested_in, getrecipients):
        self.interested_in = interested_in
        self.getrecipients = getrecipients
        
    def handle(self, message):
        """Send multipart mail."""
        if (not self.interested_in(message)):
            return None
        recipients = self.getrecipients(message)
        if len(recipients) == 0:
            return None
        msg = MIMEMultipart('alternative')
        msg['Subject'] = message.title
        msg['From'] = SENDER_MAIL
        content = message.content_plain.encode('utf-8')
        part1 = MIMEText(content, 'plain', 'utf-8')
        content = message.content.encode('utf-8')
        part2 = MIMEText(content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        smtp = smtplib.SMTP(SMTP_SERVER)
        smtp.sendmail(SENDER_MAIL, recipients, msg.as_string())
        smtp.close()
        
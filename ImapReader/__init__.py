# /* Imports */
import imaplib,os,email
from email.header import decode_header

# /* Exceptions */
class NotLoggedException(Exception):pass

# /* Main class */
class ImapReader: 
    def __init__(self):
        self.logged_in = False
    def clean(text):
        return "".join(c if c.isalnum() else "_" for c in text)
    def login(self,email:str,password:str):
        if (("outlook" in email.split('@')[-1])or("hotmail" in email.split('@')[-1])):
            self.instance = imaplib.IMAP4_SSL('imap-mail.outlook.com',993)
        elif ("aol.com" in email.split('@')[-1]):
            self.instance = imaplib.IMAP4_SSL("imap.aol.com",993)
        elif ("yahoo" in email.split('@')[-1]):
            self.instance = imaplib.IMAP4_SSL("imap.mail.yahoo.com",993)
        elif ("@mail.com" in email):
            self.instance = imaplib.IMAP4_SSL("imap.mail.com",993)
        elif ("onet.pl" in email.split("@")[-1]):
            self.instance = imaplib.IMAP4_SSL("imap.poczta.onet.pl",993)
        elif ("op.pl" in email.split("@")[-1]):
            self.instance = imaplib.IMAP4_SSL("imap.poczta.onet.pl",993)
        else:
            self.instance = imaplib.IMAP4_SSL("imap.gmail.com",993)
        try:
            self.instance.login(email,password)
            self.logged_in = True
        except Exception as e:
            print(e)
    def GetEmails(self,quantity:int):
        if self.logged_in:
            status, messages = self.instance.select("INBOX")
            # number of top emails to fetch
            emails = []
            # total number of emails
            messages = int(messages[0])
            for i in range(messages, messages-quantity, -1):
                # fetch the email message by ID
                res, msg = self.instance.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode(encoding)
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    pass
                                elif "attachment" in content_disposition:
                                    # download attachment
                                    filename = part.get_filename()
                                    if filename:
                                        folder_name = self.clean(subject)
                                        if not os.path.isdir(folder_name):
                                            # make a folder for this email (named after the subject)
                                            os.mkdir(folder_name)
                                        filepath = os.path.join(folder_name, filename)
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                    emails.append({
                        "Content":body,
                        "Content_Type":content_type,
                        "From":From,
                        "Subject":subject,
                        "Email_ID":str(i),
                        })
            return emails
        else:
            raise NotLoggedException("You must be logged in to read emails!")
    def Recent_Email(self):
        if self.logged_in:
            status, messages = self.instance.select("INBOX")
            # number of top emails to fetch
            emails = []
            N = 2
            # total number of emails
            messages = int(messages[0])
            for i in range(messages, messages-N, -1):
                # fetch the email message by ID
                res, msg = self.instance.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode(encoding)
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    pass
                                elif "attachment" in content_disposition:
                                    # download attachment
                                    filename = part.get_filename()
                                    if filename:
                                        folder_name = self.clean(subject)
                                        if not os.path.isdir(folder_name):
                                            # make a folder for this email (named after the subject)
                                            os.mkdir(folder_name)
                                        filepath = os.path.join(folder_name, filename)
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                    emails.append({
                        "Content":body,
                        "Content_Type":content_type,
                        "From":From,
                        "Subject":subject,
                        "Email_ID":str(i),
                        })
            return emails
        else:
            raise NotLoggedException("You must be logged in to read emails!")
#<-- class for the package name, description etc
class SpammerTool:
    def __version__():
        return "0.0.1"
    def __name__():
        return "Smtp Spammer"
    def __author__():
        return """web-automation-italia (C) | web-automation-uk
        
        - copyright: do not sell this code, it's completely free on @automation-it0 github page!
        """
    def __desc__() -> str:
        """*SSL EMAIL SPAMMER*

        :params:

            - login

            >>> email = Any:str

            >>> password = Any:str

            >>> port = Any:int # <-- optional -->

            >>> session = login(email|username,password,port=(default:465|custom:int),custom_smtp=None|str)

            - spam

            >>> target = Any:str

            >>> message = Any:str

            >>> times = Any:int

            >>> session->SmLib.spam(target,message,times,*args) /*!Uses threading!*/
        """
        return """*SSL EMAIL SPAMMER*

        :params:

            - login

            >>> email = Any:str

            >>> password = Any:str

            >>> port = Any:int # <-- optional -->

            >>> session = login(email|username,password,port=(default->465|custom->int),custom_smtp=None|str)

            - spam

            >>> target = Any:str

            >>> message = Any:str

            >>> times = Any:int

            >>> session->SmLib.spam(target,message,times,*args) /*!Uses threading!*/
        """

# <--!important. Imported modules !-->
import smtplib, ssl as connection_ssl,pandas as p
from threading import Thread

# <--!main, loaded all functions here !-->

"<Exceptions>"
class NoServerSpecified(Exception):pass

"<Real code>"
class SmLib(smtplib.SMTP_SSL):
    def Spam(self,target,message,times,*args):
        for i in range(times):
            Thread(target=lambda:self.send_message(message,self.user,target,*args)).start()
    def login(self,email,password,port=465,custom_smtp=None):
        context = connection_ssl.create_default_context()
        ssl = email.split("@")[-1]
        if ssl == "outlook.com" or ssl == "hotmail.com":
            with SmLib("smtp.office365.com", port, context=context) as server:
                server.login(email, password)
                self.server = server
        elif ssl == "onet.pl" or ssl == "op.pl":
            with SmLib("imap.poczta.onet.pl", port, context=context) as server:
                server.login(email, password)
                self.server = server
        elif "zoho" in ssl:
            with SmLib("smtp.zoho.eu", port, context=context) as server:
                server.login(email, password)
                self.server = server
        elif "yahoo" in ssl:
            with SmLib("smtp.mail.yahoo.com", port, context=context) as server:
                server.login(email, password)
                self.server = server
        elif "icloud" in ssl:
            with SmLib("smtp.mail.me.com", 587, context=context) as server:
                server.login(email, password)
                self.server = server
        elif "aol" in ssl.lower():
            with SmLib("smtp.aol.com", port, context=context) as server:
                server.login(email, password)
                self.server = server
        elif "mail.com" in ssl.lower():
            with SmLib("smtp.mail.com", 587, context=context) as server:
                server.login(email, password)
                self.server = server
        elif "gmail.com" in ssl.lower():
            with SmLib("smtp.gmail.com", port, context=context) as server:
                server.login(email, password)
                self.server = server
        else:
            if custom_smtp is None:
                raise NoServerSpecified("domain not found, got argument custom_smtp as None")
            else:
                with SmLib(custom_smtp, port, context=context) as server:
                    server.login(email, password)
                    self.server = server
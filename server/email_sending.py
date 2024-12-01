from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from typing import Dict, Literal
from mongo_schemas.transaction_schema import Transaction



"""
This class deals with sending emails, generating HTML for emails and parsing user data to pass into said HTML


(they all go to spam lol)
"""
class EmailSender:

    def __init__(self, sender):
        self.sender = sender
    
    def send_email(self, to_email:str, subject:str, content:str) -> None:
        """
        sends email to given sender using verified email

        args:
            to_email: duh
            subject: duh
            content: html !!
        returns nothing really :O
        """
        message = Mail(
            from_email=self.sender,  # verified sendgrid email id
            to_emails=to_email,
            subject=subject,
            html_content=content)
        
        try:
            load_dotenv()
            sg = SendGridAPIClient(os.getenv("SENDGRID_KEY"))
            response = sg.send(message)
            print(f'Status Code: {response.status_code}')
        except Exception as e:
            print(f'Error: {e}')


    def render_html(self, data: Dict[Literal["incoming", "outgoing"], Transaction]) -> tuple[str, str]:
        """

        returns: needs to return the html for the email content, but also needs to return subject line
        """
        final = []
        final.append("""
        <html>
        <head>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1, h2 { color: #333; }
            .money-in { color: green; }
            .money-out { color: red; }
            .transaction-date { color: #666; font-size: 0.9em; }
            ol { padding-left: 20px; }
            li { margin: 10px 0; }
        </style>
        </head>
        <body>
        """)
        print(data.keys())
        final.append("<h1>Transaction Summary</h1>\n")
        final.append("<h2>Money In 💰</h2>\n")
        final.append("<ol>\n")
        for transaction in data["incoming"]:
            final.append(
                f'<li><span class="money-in">${abs(transaction.amount):.2f}</span> - '
                f'{transaction.name} '
                f'<span class="transaction-date">({transaction.date})</span></li>\n'
            )
        final.append("</ol>\n")

        final.append("<h2>Money Out 📊</h2>\n")
        final.append("<ol>\n")
        for transaction in data["outgoing"]:  # Fixed the variable name
            final.append(
                f'<li><span class="money-out">-${abs(transaction.amount):.2f}</span> - '
                f'{transaction.name} '
                f'<span class="transaction-date">({transaction.date})</span></li>\n'
            )
        final.append("</ol>")
        final.append("</body></html>")

        return ("Report for today!", "".join(final))


        

# sender = EmailSender("kgubba@wisc.edu")
# one, two = sender.render_html({})
# sender.send_email("krishivgubba626@gmail.com", one, two)
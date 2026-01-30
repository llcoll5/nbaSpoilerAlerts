from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class Sender:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send_email(self, subject, html_content, receiver):
        # Crear un missatge multipart per al correu
        new_message = MIMEMultipart("alternative")
        new_message["From"] = self.username
        new_message["To"] = receiver
        new_message["Subject"] = subject

        # Afegir contingut HTML
        html_part = MIMEText(html_content, "html")
        new_message.attach(html_part)

        try:
            # Connexió amb el servidor SMTP de Gmail
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()  # Iniciar connexió segura
                connection.login(self.username, self.password)
                connection.sendmail(self.username, receiver, new_message.as_string())
                print("El correu s'ha enviat correctament!")
        except Exception as e:
            print(f"Error enviant el correu: {e}")



if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVERS")

    sender = Sender(username, password)
    subject = "Prova d'enviament de correu"
    html_content = "<h1>Això és una prova</h1><p>Correu enviat des de Python.</p>"
    sender.send_email(subject, html_content, receiver)
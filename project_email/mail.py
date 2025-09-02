import asyncio
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
from project_util import getEnviromentVariable
from .email_model import content_email_id_password_model

load_dotenv()
EMAIL_ID: str = getEnviromentVariable("EMAIL_ID")
EMAIL_PASSWORD: str = getEnviromentVariable("EMAIL_PASSWORD")


def blocking_send(to_email: str, subject: str, content: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ID
    msg["To"] = to_email
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ID, EMAIL_PASSWORD)
        smtp.send_message(msg)


async def send_email_async(to_email: str, subject: str , password:str) -> None:
    await asyncio.to_thread(blocking_send, to_email, subject, content_email_id_password_model(to_email ,password))

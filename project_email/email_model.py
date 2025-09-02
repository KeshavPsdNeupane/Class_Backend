from email.message import EmailMessage


def content_email_id_password_model(email: str, password: str) -> str:
    msg = "Dear user,\n\n" \
          "Your account for the school app has been created.\n\n" \
          "Email = " + email + "\n" \
          "Password = " + password + "\n\n" \
          "Regards,\n" \
          "Admin, Certain School"
    return msg
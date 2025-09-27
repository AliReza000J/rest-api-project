from maileroo import MailerooClient, EmailAddress
import os
from dotenv import load_dotenv
import jinja2

load_dotenv()

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(tenplate_filename, **context):
    return template_env.get_template(tenplate_filename).render(**context)


def send_simple_email(to, username, subject, body, html=None):
    api = os.getenv('MAILEROO_API_KEY')
    if not api:
        raise ValueError("MAILEROO_API_KEY is not set in environment variables")
    
    client = MailerooClient(api)

    try:
        email_data = {
            "from": EmailAddress("noreply@25d346ff4380bf05.maileroo.org", "STORES API"),
            "to": [EmailAddress(to, username)],
            "subject": subject,
            "plain": body
        }

        if html:
            email_data["html"] = html

        response = client.send_basic_email(email_data)
        return response
    except Exception as e:
        print("Error sending email:", e)
        return None



def send_user_registration_email(email,username):
    return send_simple_email(
        email,
        username,
        "Succesfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores REST API.",
        render_template("email/action.html", username=username)
    )



def send_password_reset_email(email, username, reset_url):
    subject = "Reset your password"
    text_body = f"Hi {username},\nUse the link below to reset your password:\n{reset_url}\nIf you didn’t request this, you can ignore this email."
    html_body = render_template(
        "email/password_reset.html",
        username=username,
        reset_url=reset_url,
    )
    return send_simple_email(email, username, subject, text_body, html_body)
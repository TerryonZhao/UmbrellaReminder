import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from src.fetch_weather import load_config

def load_template(template_name: str) -> str:
    """Load the email template from the specified file

    :param str template_name: Name of the email template file
    :return str: Content of the email template
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
    template_path = os.path.join(base_dir, 'email_templates', template_name)
    print(f"Loading template from: {template_path}")
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def format_rain_hours(hours: List[str]) -> str:
    """Format the rain hours into a readable string

    :param list hours: List of rain hours
    :return str: Formatted string of rain hours
    """
    if not hours:
        return "No rain expected today."
    return ", ".join(hours)

def render_template(template_name: str, rain_info: Dict) -> str:
    """Render the email template with rain information

    :param str template_name: Name of the email template file
    :param dict rain_info: Output from rain_process function containing rain details
    :return str: Rendered HTML content for the email
    """
    try:
        template = load_template(template_name)
        template_data = {
            'rain_hours': format_rain_hours(rain_info['rain_hours']),
            'total_hours': rain_info['summary']['total_hours'],
            'peak_time': rain_info['peak_rain']['time'],
            'peak_amount': rain_info['peak_rain']['amount']
        }

        return template.format(**template_data)
    except FileNotFoundError:
        print(f"Error: Template file '{template_name}' not found.")
        return ""
    except KeyError as e:
        print(f"Error: Missing key in template data - {e}")
        return ""
    except Exception as e:
        print(f"Error rendering template: {e}")
        return ""

def smtp_send(config: dict, subject: str, html_content: str) -> bool:
    """Send an email using SMTP

    :param dict config: email config
    :param str subject: Subject of the email
    :param str html_content: HTML content of the email
    :return bool: True if email sent successfully, False otherwise
    """
    email_config = config['email']
    try:
        email = MIMEMultipart("alternative")
        email["Subject"] = subject
        sender_name = email_config.get("sender_name", "UmbrellaReminder")
        email["From"] = f"{sender_name} <{email_config['sender_email']}>"
        email["To"] = email_config["recipients"]

        email_content = MIMEText(html_content, "html", "utf-8")
        email.attach(email_content)
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            server.send_message(email)
            server.quit()
        print("Email sent successfully.")
        return True
    except smtplib.SMTPConnectError:
        print(f"SMTP Connect Error")
        return False

def send_rain_email(rain_info: Dict) -> bool:
    """Excute the email sending process according to rain information
    
    :param dict rain_info: Output from rain_process function containing rain details
    :return bool: True if email sent successfully, False otherwise
    """
    worst_level = rain_info['summary']['worst_level']

    if worst_level == "no":
        print("No rain expected today. No email will be sent.")
        return False

    template_map = {
        'light': 'light_rain_template.html',
        'moderate': 'moderate_rain_template.html',
        'heavy': 'heavy_rain_template.html'
    }

    try:
        template_name = template_map.get(worst_level)
        html_content = render_template(template_name, rain_info)
        config = load_config()
        subject = f"降雨提醒 - {worst_level.capitalize()} Rain"
        smtp_send(config, subject, html_content)
        print(f"Use template: {template_name}")
        return True
    except FileNotFoundError:
        print(f"Error: Configuration or template file not found.")
        return False

if __name__ == "__main__":
    # Test
    test_rain_info = {
        'has_rain': True,
        'rain_hours': ['09:00', '14:00', '18:00'],
        'summary': {
            'total_hours': 3,
            'worst_level': 'light'
        },
        'peak_rain': {
            'time': '14:00',
            'level': 'light',
            'amount': 2.5
        }
    }
    send_rain_email(test_rain_info)
from twilio.rest import Client

# Function to get reports edited in the last 24 hours
from datetime import datetime, timedelta

from models.report import Report
from models.subscription import Subscription


def get_reports_edited_in_last_day():
    now = datetime.utcnow()
    last_day = now - timedelta(days=1)
    reports = Report.query.filter(Report.updated_at >= last_day).all()
    return reports


# Function to get all subscribers
def get_subscribers():
    subscriptions = Subscription.query.all()
    phone_numbers = [sub.phone_number for sub in subscriptions]
    return phone_numbers


# Function to send a text message using Twilio
def send_text_message(to_phone_number, message):
    try:
        account_sid = 'ACb0036bfab6e583cf62efe72b1c8d9d15'
        auth_token = '1a0116175cd04101f8f81982878057ac'
        twilio_number = '+15206756943'  # Your Twilio phone number
        target_number = '+16479818740'  # The number you want to send the SMS to

        # Create the client
        client = Client(account_sid, auth_token)

        # Send the SMS
        message = client.messages.create(
            body="Hello One of your reports have been updated",
            from_=twilio_number,
            to=target_number
        )

        print(f"Message sent! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {to_phone_number}: {e}")


# Function to send notifications about edited reports
def send_notifications():
    reports = get_reports_edited_in_last_day()

    if not reports:
        print("No reports were edited in the last 24 hours.")
        return

    phone_numbers = get_subscribers()

    for report in reports:
        message = f"Report '{report.name}' has been updated. Description: {report.description}. Check it out!"
        for phone_number in phone_numbers:
            send_text_message(phone_number, message)


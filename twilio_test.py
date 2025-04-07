from twilio.rest import Client

# Replace with your Twilio account details
account_sid = 'ACb0036bfab6e583cf62efe72b1c8d9d15'
auth_token = '1a0116175cd04101f8f81982878057ac'
twilio_number = '+15206756943'       # Your Twilio phone number
target_number = '+16479818740'       # The number you want to send the SMS to

# Create the client
client = Client(account_sid, auth_token)

# Send the SMS
message = client.messages.create(
    body="Hello from Python using Twilio!",
    from_=twilio_number,
    to=target_number
)

print(f"Message sent! SID: {message.sid}")

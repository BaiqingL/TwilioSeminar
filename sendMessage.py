from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "[no]"
auth_token = "[no]"

client = Client(account_sid, auth_token)

client.api.account.messages.create(
    to="+[number]",
    from_="+[twilio_number]",
    body="Hello There")

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    actualmsg = request.values.get('Body', None)
    body = actualmsg.lower()
    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")
    else:
        resp.message("I didn't understand '" + actualmsg + "' my programmer hasn't taught me that yet")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
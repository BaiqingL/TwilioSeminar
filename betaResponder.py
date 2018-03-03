from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from random import randint
import feedparser

app = Flask(__name__)


def parseRSS(rss_url):
    return feedparser.parse(rss_url)


def getHeadlines(rss_url):
    headlines = []
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines


allheadlines = []


newsurls = {'local': 'http://wellesley.wickedlocal.com/sports/high-school?template=rss&mime=xml'}
for key, url in newsurls.items():
    # Call getHeadlines() and combine the returned headlines with allheadlines
    allheadlines.extend(getHeadlines(url))

# Jokes array, J1 is the first section and J2 is the second response
j1 = ["Why do cows have hooves instead of feet?", "If I bought a balloon for $0.99..."]
j2 = ["Because they lactose", "how much should I sell it for when I adjust for inflation?"]

persons = []
prev = []


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    actualmsg = request.values.get('Body', None)
    p = request.values.get('From', None)
    if p not in persons:
        persons.append(p)
        prev.append([])

    i = persons.index(p)

    body = actualmsg.lower()
    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message

    if body == 'hello' or body == 'hi':
        rsp(i, resp, "Hi! What is your name?")
    elif prev[i][len(prev[i]) - 1] == "Hi! What is your name?":
        rsp(i, resp, "Nice to meet you " + actualmsg + ". I am Mike. How are you doing?")
    elif "How are you doing?" in prev[i][len(prev[i]) - 1]:
        if "good" in body or "great" in body:
            rsp(i, resp, "I'm glad to hear that!")
        elif "bad" in body or "sad" in body:
            rsp(i, resp, "I'm sad to hear that!")
        else:
            rsp(i, resp, "That's ok, I guess!")
    elif body == "what is the news?":
        rsp(i, resp, allheadlines)
    elif body == "tell me a joke":
        j = randint(0, len(j1) - 1)
        rsp(i, resp, j1[j])
        rsp(i, resp, j2[j])
    elif body == 'bye':
        rsp(i, resp, "Goodbye! I will forget what you just said.")
        del prev[i][:]

    else:
        # Just in case the bot doesn't understand
        rsp(i, resp, "I didn't understand '" + actualmsg + "' my programmer hasn't taught me that yet")

    print(prev[i])

    return str(resp)


def rsp(i, resp, ins):
    prev[i].append(ins)
    resp.message(ins)


if __name__ == "__main__":
    app.run(debug=True)

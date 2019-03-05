import feedparser
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from random import randint
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)


def parseRSS(rss_url):
    return feedparser.parse(rss_url)


def getHeadlines(rss_url):
    headlines = []
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines

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
    try:
        if body == 'hello' or body == 'hi':
            rsp(i, resp, "Hi! What is your name?")
        elif prev[i][len(prev[i]) - 1] == "Hi! What is your name?":
            rsp(i, resp, "Nice to meet you " + actualmsg + ". I am a chatbot. How are you doing?")
        elif "How are you doing?" in prev[i][len(prev[i]) - 1]:
            if "good" in body or "great" in body:
                rsp(i, resp, "I'm glad to hear that!")
            elif "bad" in body or "sad" in body:
                rsp(i, resp, "I'm sad to hear that!")
            else:
                rsp(i, resp, "That's ok, I guess!")
        elif body == "what is the news?":
            rsp(i, resp, allheadlines[0])
            rsp(i, resp, "Do you want me to keep going?")
        elif "Do you want me to keep going?" in prev[i][len(prev[i]) - 1]:
            if "yes" in body or "y" in body or "sure" in body:
                rsp(i, resp, allheadlines[1])
            else:
                rsp(i, resp, "Ok, today was boring I guess")
        elif body == "tell me a joke":
            j = randint(0, len(j1) - 1)
            rsp(i, resp, j1[j])
            rsp(i, resp, j2[j])
        elif body == 'bye':
            rsp(i, resp, "Goodbye! I will forget what you just said.")
            del prev[i][:]
        else:
            # Just in case the bot doesn't understand
            rsp(i, resp, str(chatbot.get_response(actualmsg)))
    except:
        rsp(i, resp, str(chatbot.get_response(actualmsg)))
    print(prev[i])
    
    return str(resp)


def rsp(i, resp, ins):
    prev[i].append(ins)
    resp.message(ins)

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

# Let's train the bot using the server logs
chatbot = ChatBot('AI')
trainer = ListTrainer(chatbot)
trainer.train(str(open("logs.txt","r").read()).split("\n"))

if __name__ == "__main__":
    app.run(debug=True)

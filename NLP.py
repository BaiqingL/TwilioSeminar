from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import time

# Create a new chat bot named Charlie
chatbot = ChatBot('AI')

trainer = ListTrainer(chatbot)

trainer.train(str(open("logs.txt","r").read()).split("\n"))

response = input()
while 1==1:
	response = chatbot.get_response(response)
	time.sleep(0.5)
	print(response)

import requests
bot_message = ""

while bot_message != "It was nice talking to you! good bye":

	message = input('Agent: ')
	r = requests.post('http://localhost:5003/webhooks/rest/webhook', json={'message': message})

	print('Bot: ', end='')
	for i in r.json():
		bot_message = i['text']
		print(f"{i['text']}")

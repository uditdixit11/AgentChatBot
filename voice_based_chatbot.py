import requests
import speech_recognition as sr
from gtts import gTTS
from time import sleep
import pyglet
import os
import warnings
warnings.filterwarnings("ignore")

# System call
os.system("")
# Class of different styles
class style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    WHITE = '\033[37m'

bot_message = ""
message = ""
counter = 0

print(style.WHITE +"Welcome to HR Voice Based Assistance..")
while bot_message != "It was nice talking to you! good bye":

    # Speech to text
    r = sr.Recognizer()
    flag = True
    with sr.Microphone() as source:
        try:
            print(style.BLUE +"Agent: ", end="")
            audio = r.listen(source, timeout=10)
            message = r.recognize_google(audio)
            print(style.GREEN+ message)
        except:
            flag = False
            print(style.RED +"Sorry couldn't recognize the voice")

    if len(message) == 0 or flag == False:
        continue

    r = requests.post('http://localhost:5003/webhooks/rest/webhook', json={'message': message})
    print(style.BLUE + 'Bot: ', end='')

    # if there is something out of the context query, for our nlu model couldn't recognize the intent
    if r.json() == []:
        print(style.RED +"Couldn't understand, Please raise a ticket at the Employee Support portal.")

    # Text to speech
    inner_counter = 0
    for i in r.json():
        bot_message = i['text']
        print(style.YELLOW +f"{i['text']}")
        language = "en"

        myObj = gTTS(text=bot_message, lang=language)
        filename = os.path.join('chatbot_audios', '1_'+str(counter)+str(inner_counter)+'.wav')
        myObj.save(filename)

        music = pyglet.media.load(filename, streaming=False)
        music.play()

        # prevent from killing
        sleep(music.duration)
        inner_counter += 1

    counter += 1


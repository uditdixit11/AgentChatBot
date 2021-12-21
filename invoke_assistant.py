import speech_recognition as sr

speech_invoke_commands = ['hello hr', 'hr', 'h.r.', 'h r', 'ok hr', 'o k h r', 'okhr', 'ok achar']
counter=0
while True:
    print(counter)
    r = sr.Recognizer()
    flag = True
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            message = r.recognize_google(audio)
            if message.lower() in speech_invoke_commands:
                import voice_based_chatbot

        except:
            flag = False
            print("Sorry couldn't recognize the voice")

    counter+=1

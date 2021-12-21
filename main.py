##############################################################################
# Developed by: Shobhit Agarwal
# Note: Using Socket, Rasa
# Algorithm:
# 1.) create a flask app
# 2.) Run the application using socket for real time experience between agent and the customer screen.
# 3.) After running main.py, open http://127.0.0.1:5000/ and http://127.0.0.1:5000/customer
# on different tabs in Web browser.
# 4.) Run following two commands in cmd:
# 4.1) rasa run actions: This command is used to run external functionalities.
# 4.2) rasa run -m models --endpoints endpoints.yml --port 5003 --credentials credentials.yml --enable-api
# A model is loaded and the predictions for the input starts.
# 5.) We can now get the suggestions on the agent screen based on the inputs from customer.
##############################################################################

# Import Modules
from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import Global_var
from emotion_analysis import extract_emotion

suggestion_list = []
# Create Flask Application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO(app)

@app.route( '/' )
def agent():
    '''
        Opens up Agent Webpage at http://127.0.0.1:5000/
    '''
    return render_template('agentAppPage.html', person=Global_var.person, mobile=Global_var.mobile)

@app.route( '/customer' )
def customer():
    '''
        Opens up Customer Webpage at http://127.0.0.1:5000/customer
    '''
    return render_template('customerAppPage.html')

def messageRecived():
  print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json):
  global suggestion_list
  flag = False
  for i, j in json.items():
    if i == "data":
      flag = False
    else:
      flag = True

  # Message received flag is True
  if flag == True:

    # find the emotion from the text
    emotion_is = extract_emotion(json['message'])
    # Send the message to the localhost:5003, where model resides and returns the response in res variable
    res = requests.post('http://localhost:5003/webhooks/rest/webhook', json={'message': json['message']})
    res = res.json()
    try:
        if res == [] and json['message'] == "":
            socketio.emit('my same response', suggestion_list[-1], callback=messageRecived)
        # This condition is for sending the response directly with one click
        elif json['message'] != "" and res == []:
            socketio.emit('suggestion response', {'recipient_id': 'default',
                                                  'text': 'The question is not in my knowledge database, Transfer call to your supervisor'},
                          callback=messageRecived)
            socketio.emit('my response', json, callback=messageRecived)
            socketio.emit('emotion response', emotion_is, callback=messageRecived)

        else:
            val = res[0]['text']
            suggestion_list.append(res[0])
            socketio.emit('suggestion response', res[0], callback=messageRecived)
            socketio.emit('my response', json, callback=messageRecived)
            socketio.emit('emotion response', emotion_is, callback=messageRecived)
    except:
        socketio.emit('my response', json, callback=messageRecived)
  else:
    socketio.emit('my response', json, callback=messageRecived)

if __name__ == '__main__':
    socketio.run(app, debug=True)

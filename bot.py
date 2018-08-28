from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage
import os

app = Flask(__name__)
kik = KikApi("chinyeebot", "8ed8ec43-b3c6-45d9-85e4-0e4442d592a4")

kik.set_configuration(Configuration(webhook="https://chinyeebot.herokuapp.com/incoming"))

#("Hi, I'm your rating lunch bot, if you wanna rate your lunch, type\"rate lunch\", if you wanna see the menu, type\"see menu\"")

@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)
    messages = messages_from_json(request.json['messages'])
    print(messages)
    for message in messages:
        if isinstance(message, TextMessage):
            if message.body.lower() == "rate lunch":
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Here is your lunch menu:")])# need to get the lunch view from database
            elif message.body.lower() == "see menu":
            	kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Here is your lunch menu:")])#need to communicate with database
            else:
                kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="I don't understand, please try again")])# need to reset the conversation and start over
        return Response(status=200)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)



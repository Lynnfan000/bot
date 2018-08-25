from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage
import os

print("start")
app = Flask(__name__)
kik = KikApi("chinyeebot", "8ed8ec43-b3c6-45d9-85e4-0e4442d592a4")

print("will set config")
kik.set_configuration(Configuration(webhook="https://chinyeebot.herokuapp.com/incoming"))


@app.route('/incoming', methods=['POST'])
def incoming():
    print("incoming")
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, TextMessage):
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body+"chenlixiangdashabi"
                )
            ])

    return Response(status=200)

print("will run")
# if __name__ == "__main__":
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
# app.run(port=int(os.environ['PORT']), debug=False)
print("ran")



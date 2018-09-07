from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage
import os
import sys
import mysql.connector
from datetime import date



class mymenu:
    def __init__(self, date, menu):
        self.date = date
        self.menu = menu
my_date = date.today()


app = Flask(__name__)
kik = KikApi("chinyeebot", "8ed8ec43-b3c6-45d9-85e4-0e4442d592a4")
mydb = mysql.connector.connect(
  host="us-cdbr-iron-east-01.cleardb.net",
  user="b68cd089abc81d",
  passwd="2c2f1c38",
  database="heroku_5a951cfac26923b"
)
mycursor = mydb.cursor()
#sql = "select menu from menu join lunch_info on lunch_info.menu_id=menu.id where date=?"

mycursor.execute("select menu from menu join lunch_info on lunch_info.menu_id = menu.id where lunch_info.date = %(date)s", {'date': my_date})
#mycursor.execute("select menu from menu")
my_menu=mycursor.fetchall()

today = mymenu(my_date, my_menu)

kik.set_configuration(Configuration(webhook="https://chinyeebot.herokuapp.com/incoming"))
state=0

@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)
    messages = messages_from_json(request.json['messages'])
    for message in messages:
        if isinstance(message, TextMessage):
            if state==1: #this is a comment from user      
                sql = "INSERT INTO comment (date, menu, name, comment) VALUES (%s, %s, %s, %s)"
                val = (my_date, my_menu, message.from_user, message.body)
                mycursor.execute(sql, val)
                mydb.commit()
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Okay, got that!")])
                state = 0
            elif message.body.lower() in ["hi", "hello", "hi!", "hello!", "hey"]:
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Hi, I'm your rating lunch bot, if you wanna rate your lunch, type\"rate lunch\", if you wanna see the menu, type\"see menu\"")])
                state = 0
            elif message.body.lower() == "rate lunch":
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Here is your lunch menu: "+my_menu)])
                state = 1
            elif message.body.lower() == "see menu":
            	kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Here is your lunch menu: "+my_menu)])#need to communicate with database
            	state = 0
            else:
                kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="I don't understand, you can type\"rate lunch\" to rate your lunch or \"see menu\" to see the menu")])
                state=0
        return Response(status=200)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) #everything will not run after this line
    



from flask import Flask

app = Flask(__name__)

@app.route('/')
def source():
 html = 'Hello World!'
 return html

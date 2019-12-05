from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return 'Welcome to TwitOff!'
from flask import Flask, render_template, request
from .model import init, prediction_msg


#def create_app():
app = Flask(__name__)
classifier = init()
    #return app


import chatbot.chat

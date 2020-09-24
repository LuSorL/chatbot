from flask import Flask, render_template, request
from .model import init, prediction_msg
#import .
from chatbot import app
messages = []
reponses = []

@app.route('/')
def index():
    return render_template('index.html', message = messages, reponse = reponses)

@app.route('/', methods=["POST", "GET"])
def index_msg():
    global messages, reponses
    message = request.form.get("message_input")
    messages.append(message)
    attente = prediction_msg(message)
    if attente[0] == 'autre':
        reponses.append('Je ne suis pas capable de répondre à votre demande')
    else :
        reponses.append("Je lance l'impresion du document ")

    return render_template('index.html', message = messages, reponse = reponses)

if __name__ == "__main__":
    app.run()

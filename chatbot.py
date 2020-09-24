from flask import Flask, render_template, request
import model
import .
messages = []
reponses = []

@app.route('/', methods=["POST", "GET"])
def index():
    global messages, reponses
    message = request.form.get("message_input")
    messages.append(message)
    attente = model.prediction_msg(message)
    if attente[0] == 'autre':
        reponses.append('Je ne suis pas capable de répondre à votre demande')
    else :
        reponses.append("Je lance l'impresion du document ")

    return render_template('index.html', message = messages, reponse = reponses)

if __name__ == "__main__":
    app.run()

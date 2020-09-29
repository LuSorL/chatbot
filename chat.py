from flask import Flask, render_template, request
from .model import init, prediction_msg
from chatbot import app
import xlrd
import xlwt
from xlutils.copy import copy
from time import strftime
from datetime import datetime
from datetime import timedelta
import json

#initialisation liste des messages et réponses
messages = []
reponses = []


#classifier = subprocess(init())


@app.route('/')
def index():
    return render_template('index.html', message = messages, reponse = reponses)

@app.route('/', methods=["POST", "GET"])
def index_msg():
    global messages, reponses, is_empty
    message = request.form.get("message_input")
    date = datetime.now()
    msg_day = date.isoweekday()
    time = date.strftime("%m/%d/%Y %H:%M:%S")
    day = date.strftime("%m/%d/%Y")
    msg_hour = date.hour
    msg_min = date.minute
    messages.append(message)

    #attente = prediction_msg(message, classifier)
    attente = ['aud']
    if attente[0] == 'autre':
        reponses.append('Je ne suis pas capable de répondre à votre demande')
    else :
        #récupération du nombre de pages
        list_pages = message.split("pages", 1)
        list_pages_bis = list_pages[0].split()
        nb_pages = list_pages_bis[-1]

        #récupération du nom du document
        list_doc = message.split("doc", 1)
        list_doc_bis = list_doc[1].split()
        nom_doc = "doc"+list_doc_bis[0]



        #ouverture JSON

        file = open("./chatbot/calendrier.json", "r")
        json_file = json.load(file)
        file.close()

        #calcul timing
        pages = int(nb_pages)


        if len(json_file) == 0:
            start = time
        else:
            if (date - datetime.strptime(day + " 19:00:00", "%m/%d/%Y %H:%M:%S")).seconds > pages:
                late = datetime.strptime(json_file[-1]["end"], "%m/%d/%Y %H:%M:%S")
                if (date - late).days == 0:
                    start = max(date, late).strftime("%m/%d/%Y %H:%M:%S")
                else:
                    for i in range(len(json_file), 0, -1):
                        elem = datetime.strptime(json_file[i-1]['end'], "%m/%d/%Y %H:%M:%S")
                        if (elem.day == date.day):
                            if (elem - elem.replace(hour = 19, minute = 00, second = 00)).seconds > pages:
                                start = elem.strftime("%m/%d/%Y %H:%M:%S")
                                break
            else:
                late = datetime.strptime(json_file[-1]["end"], "%m/%d/%Y %H:%M:%S")
                if (date - late).days == 0:
                    day_after = date.day +1
                    start = date.replace(day = day_after, hour = 7, minute = 0, second = 0, microsecond = 0)
                else:
                    start = late.replace(second = late.seconds + 1)


        end = datetime.strptime(start, "%m/%d/%Y %H:%M:%S") + timedelta(seconds = pages)



        #Update json
        object = {}
        object['titre'] = nom_doc
        object['utilisateur'] = "toto" #a modifier
        object['start'] = start
        object['end'] = end.strftime("%m/%d/%Y %H:%M:%S")

        json_file.append(object)

        #ecriture JSON
        file = open("./chatbot/calendrier.json", "w")
        json.dump(json_file, file)
        file.close()

        #envoie message de réponse
        reponses.append("Je lance l'impresion du document doc" + nom_doc + " de " + nb_pages + "pages")
    return render_template('index.html', message = messages, reponse = reponses)

if __name__ == "__main__":
    app.run()

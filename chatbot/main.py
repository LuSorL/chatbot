from flask import Flask,Blueprint, render_template,request,redirect,url_for, session,current_app, send_file
import os
from . import database_user as db
from os.path import basename
import pickle
import pandas as pd
import json
from time import strftime
from datetime import datetime
from datetime import timedelta
import fnmatch

main = Blueprint('main', __name__)

signed_in = False

messages = []
reponses = []
json_file = []

cwd = os.getcwd() + '/chatbot/'
filename = 'model.pkl'
with open(cwd + filename,'rb') as model :
        classifier = pickle.load(model)

def prediction_msg(msg, classifier = classifier) :
    temp = pd.DataFrame({'message' : [msg] })
    pred = classifier.predict(temp)
    return pred



@main.route('/')
@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/signup')
def signin():
    return render_template('signup.html')

@main.route('/chatbot')
def chat():
    return render_template('index.html', message = messages, reponse = reponses)

@main.route('/chatbot', methods=["GET"])
def chat_back():
    return render_template('index.html', message = messages, reponse = reponses)

@main.route('/chatbot', methods=["POST"])
def chat_msg():
    global messages, reponses, json_file
    message = request.form.get("message_input")
    date = datetime.now()
    msg_day = date.isoweekday()
    time = date.strftime("%m/%d/%Y %H:%M:%S")
    day = date.strftime("%m/%d/%Y")
    msg_hour = date.hour
    msg_min = date.minute
    messages.append(message)

    attente = prediction_msg(message, classifier)

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
        print(list_doc_bis)
        if list_doc_bis[0] == 'ument' :
            nom_doc = list_doc_bis[1]
        else :
            nom_doc = 'doc' + list_doc_bis[0]

        #ouverture JSON
        cwd = os.getcwd() + '/chatbot/static/'

        found = 0
        for filename in os.listdir(cwd) :
            if fnmatch.fnmatch(filename,"calendrier.json"):
                found = 1
                break

        if found == 0 :
            with open(cwd + "calendrier.json","w") as f :
                    json.dump([],f)

        file = open(cwd + "calendrier.json", "r")
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
        file = open(cwd + "calendrier.json", "w")
        json.dump(json_file, file)
        file.close()

        #envoie message de réponse
        reponses.append("Je lance l'impresion du document " + nom_doc + " de " + nb_pages + "pages")
    return render_template('index.html', message = messages, reponse = reponses)


@main.route('/calendrier', methods=['POST','GET'])
def calendrier():
    print("json ", json_file)
    return render_template('calendrier.html', json = json_file)

if __name__ == "__main__":
    main.run(debug = True)

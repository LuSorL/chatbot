#!/usr/bin/env python
# coding: utf-8

import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string
from nltk.corpus import stopwords
from sklearn import metrics
from sklearn import model_selection
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.tree import DecisionTreeClassifier
from spacy.lang.fr import French
import os


# Source : https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer.html

class TextStats(BaseEstimator, TransformerMixin):
    """Extract features from each document for DictVectorizer"""

    def fit(self, x, y=None):
        return self

    def transform(self, descs):
        return [{'stats_num_sentences': text.count(' ')}
                for text in descs]


class SingleColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]

class MultiColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)

        try:
            return X[self.columns].to_dict('records')
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError("The DataFrame does not include the columns: %s" % cols_error)


def split_into_lemmas_spacy(desc) :
    nlp = French()
    doc = nlp(desc)
    return [w.lemma_ for w in doc]


classifier_pipeline = None

def init():
    global classifier_pipeline
    database_path = "/Users/louismorel/Documents/cours/chatbot/chatbot/data/"

    df = pd.DataFrame()
    for filename in os.listdir(database_path):
        if not filename.startswith('.'):
            df = df.append(pd.read_excel(database_path + filename, names = ['attente','message']), ignore_index = True)

    df = df.drop_duplicates()

    X = df['message']
    X = pd.DataFrame(X)
    y = df['attente']
    y = pd.DataFrame(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)


    nltk_stopwords = stopwords.words('french')+list(string.punctuation)

    # Objet TfidfVectorizer
    msg_vectorizer = TfidfVectorizer(tokenizer=split_into_lemmas_spacy,
                                    lowercase=True,
                                    stop_words=nltk_stopwords,
                                    min_df=0.001)

    # Pipeline spécifique
    msg_pipeline = make_pipeline(
        SingleColumnSelector(key="message"),
        msg_vectorizer
    )

    # Exemple d'application de la pipeline
    msg_pipeline.fit(X_train)
    res = msg_pipeline.transform(X_test.head())

    # Affichage des traits extraits par la pipeline
    feat_names = msg_vectorizer.get_feature_names()

    stats_vectorizer = DictVectorizer()

    # Pipeline spécifique
    stats_pipeline = make_pipeline(
        SingleColumnSelector(key="message"),
        TextStats(),
        stats_vectorizer
    )

    # Exemple d'application de la pipeline
    stats_pipeline.fit(X_train)
    res = stats_pipeline.transform(X_test.head())


    # Affichage des traits extraits par la pipeline
    feat_names = stats_vectorizer.get_feature_names()

    # Union des traits
    union = FeatureUnion(transformer_list = [
            ("msg_feature", msg_pipeline),
        ("stats_features", stats_pipeline)
        ])

    # Chaîne de prétraitement globale, composée de l'union des chaînes
    preprocess_pipeline = make_pipeline(
        union
    )

    # Application de la chaîne à X_train
    preprocess_pipeline.fit(X_train)
    X_transformed = preprocess_pipeline.transform(X_train)

    #Affichage du nombre de traits générés par chacune des chaines
    fnames_msg = msg_pipeline.named_steps['tfidfvectorizer'].get_feature_names()
    fnames_stat = stats_pipeline.named_steps['dictvectorizer'].get_feature_names()


    classifier_pipeline = make_pipeline(
        preprocess_pipeline,
        RandomForestClassifier()
    )
    # Apprentissage avec les données d'entraînement
    classifier_pipeline.fit(X_train, y_train)
    # Test sur des données issues du jeu de test (uniquement les premières lignes)
    #predicted = classifier_pipeline.predict(X_test.head(20))
    #all_predictions = classifier_pipeline.predict(X_test)
    return classifier_pipeline




def prediction_msg(msg, classifier) :
    temp = pd.DataFrame({'message' : [msg] })
    pred = classifier.predict(temp)
    return pred

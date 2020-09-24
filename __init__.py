from flask import Flask, render_template, request
import model

def create_app():
    app = Flask(__name__)
    model.init()
    return app

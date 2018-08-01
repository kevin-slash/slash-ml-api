''' # -*- coding: utf-8 -*-
# __version__ = '0.1'
# import os
# from flask import Flask, session
# from flask_debugtoolbar import DebugToolbarExtension
# from flask_session import Session

# #UPLOAD_FOLDER = 'upload'
# UPLOAD_FOLDER = '/Users/lion/Documents/py-workspare/slash-ml/data/dataset/text'
# #ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.debug = True

# app.secret_key = os.getenv('SECRET_KEY') or \
# 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
# app.config['SECRET_KEY'] = app.secret_key

# app.config['SESSION_TYPE'] = 'filesystem'

# api_session = Session()
# api_session.init_app(app)

# toolbar = DebugToolbarExtension(app)

# #from slashmlapi.controllers import *
# from slashmlapi.controllers import route '''

import os
import json
from flask import Flask, session, g
#from flask_debugtoolbar import DebugToolbarExtension
from flask_session import Session
from flask import render_template, request, redirect, session, make_response
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

from flask_cors import CORS, cross_origin
from datetime import timedelta
from functools import update_wrapper
import time
from slashmlapi.config import LOG_FILE

import logging

app_globals = {}

def init_app():
    if app_globals.get('app', False):
        app = app_globals['app']
    else:
        app = Flask(__name__)

    #logfile = '/var/www/opensource/logfile.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    logging.info('ServerRun Start ML')

    # File directory
    UPLOAD_FOLDER = os.getcwd() + '/data/{session}/dataset/text'


    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #app.debug = True

    app.secret_key = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
    app.config['SECRET_KEY'] = app.secret_key

    app.config['SESSION_TYPE'] = 'filesystem'

    # Allow authorizartion header
    CORS(app)
    #cors = CORS(app, resources={r"/getresults": {"origins": "http://192.168.2.111:8000"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    #toolbar = DebugToolbarExtension(app)

    from slashmlapi.app.slashml.routes import routes
    app.register_blueprint(routes, url_prefix="/")

    return app

app = init_app()

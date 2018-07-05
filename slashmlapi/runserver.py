#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os
#from slashmlapi import app

__version__ = '0.1'
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

import logging

logfile = '/Users/lion/Documents/py-workspare/slash-ml/logfile.log'
#logfile = '/var/www/opensource/logfile.log'
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logging.info('ServerRun Start ML')

#UPLOAD_FOLDER = '/var/www/opensource/data/dataset/text'
UPLOAD_FOLDER = os.getcwd() +  '/data/dataset/text'

application = Flask('slashmlapi')

application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#application.debug = True

application.secret_key = os.getenv('SECRET_KEY') or \
'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
application.config['SECRET_KEY'] = application.secret_key

application.config['SESSION_TYPE'] = 'filesystem'

# Allow authorizartion header
CORS(application)
#cors = CORS(application, resources={r"/getresults": {"origins": "http://192.168.2.111:8000"}})
application.config['CORS_HEADERS'] = 'Content-Type'

#toolbar = DebugToolbarExtension(application)

@application.route('/')
def hello():
    info = {
        'data': 'Hello world!'
    }
    return json.dumps(info)

@application.before_request
def before_request():
    g.start_time = time.time()  # Store in g, applicable for this request and this user only


@application.route('/getresults', methods=['GET', 'POST', 'OPTIONS'])
def execute():
    if request.method == 'POST':

        from slashmlapi.controllers.result_controller import ResultController

        result_controller = ResultController(g.start_time, request, **application.config)

        _, info = result_controller.start_operation()

        time_taken = time.time() - g.start_time   # Retrieve from g
        info['com_time'] = time_taken

        return json.dumps(info)

    else:
        info = {
            'error': 'KO'
        }
        return json.dumps(info)


@application.route('/classify', methods=['GET', 'POST', 'OPTIONS'])
def classify():
    """ Classify based-on input text
    """

    if request.method == 'POST':
        from slashmlapi.controllers.predict_controller import PredictController

        # Basic configuration
        config = {
            'text_dir': 'data/dataset/chatbot',
            'dataset': 'data/matrix',
            'bag_of_words': 'data/bag_of_words',
            'train_model': 'data/model/train.model'
        }

        predict_controller = PredictController(g.start_time, request, **config)
        _, info = predict_controller.start_operation()
        logging.info(info)

        time_taken = time.time() - g.start_time   # Retrieve from g
        info['com_time'] = time_taken

        return json.dumps(info)
    else:
        info = {
            'error': 'KO'
        }
        return json.dumps(info)


if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0')

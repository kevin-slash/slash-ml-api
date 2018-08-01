import os
import json
from flask import Flask, session, g, Blueprint, request
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
import slashmlapi
import logging
routes = Blueprint('slashml', __name__)

@routes.route('/')
def hello():
    info = {
        'data': 'Hello world!'
    }
    return json.dumps(info)

@routes.before_request
def before_request():
    g.start_time = time.time()  # Store in g, applicable for this request and this user only


@routes.route('/getresults', methods=['GET', 'POST', 'OPTIONS'])
def execute():
    if request.method == 'POST':

        # Basic configuration
        config = {
            'text_dir': 'data/{session}/dataset/text',
            'archive_dir': 'data/{session}/dataset/temp',
            'dataset': 'data/{session}/matrix',
            'bag_of_words': 'data/{session}/bag_of_words',
            'train_model': 'data/{session}/model/train.model',
            'label_match': 'data/{session}/bag_of_words/label_match.pickle'
        }

        # Get headers
        headers = request.headers

        # Get session id from header
        sid = 'deadbeefbabe2c00ffee'
        for key, val in headers.items():
            if key == 'Session-Id':
                sid = val

        # Update session id
        slashmlapi.app.config['UPLOAD_FOLDER'] = slashmlapi.app.config['UPLOAD_FOLDER'].replace("{session}", sid)

        for attribute in config:
            config[attribute] = config[attribute].replace("{session}", sid)

        # Initialize Result Controller
        from slashmlapi.app.slashml.result_controller import ResultController
        result_controller = ResultController(g.start_time, request, config=config, **slashmlapi.app.config)

        _, info = result_controller.start_operation()

        time_taken = time.time() - g.start_time   # Retrieve from g
        info['com_time'] = time_taken

        return json.dumps(info)

    else:
        info = {
            'error': 'KO'
        }
        return json.dumps(info)


@routes.route('/classify', methods=['GET', 'POST', 'OPTIONS'])
def classify():
    """ Classify based-on input text
    """

    if request.method == 'POST':
        from slashmlapi.app.slashml.predict_controller import PredictController

        # Basic configuration
        config = {
            'text_dir': 'data/{session}/dataset/text',
            'archive_dir': 'data/{session}/dataset/temp',
            'dataset': 'data/{session}/matrix',
            'bag_of_words': 'data/{session}/bag_of_words',
            'train_model': 'data/{session}/model/train.model',
            'label_match': 'data/{session}/bag_of_words/label_match.pickle',
        }

        # Get headers
        headers = request.headers

        # Get session id from header
        sid = 'deadbeefbabe2c00ffee'
        for key, val in headers.items():
            if key == 'Session-Id':
                sid = val

        for attribute in config:
            config[attribute] = config[attribute].replace("{session}", sid)

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

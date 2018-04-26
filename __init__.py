# -*- coding: utf-8 -*-
__version__ = '0.1'
import os
from flask import Flask, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_session import Session

#UPLOAD_FOLDER = 'upload'
UPLOAD_FOLDER = '/Users/lion/Documents/py-workspare/slash-ml/data/dataset/text'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask('api')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug = True

app.secret_key = os.getenv('SECRET_KEY') or \
'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
app.config['SECRET_KEY'] = app.secret_key

app.config['SESSION_TYPE'] = 'filesystem'

api_session = Session()
api_session.init_app(app)

toolbar = DebugToolbarExtension(app)

from api.controllers import *

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os
#from slashmlapi import app

__version__ = '0.1'
import os
import json
from flask import Flask, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_session import Session
from flask import render_template, request, redirect, session, make_response
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename


#UPLOAD_FOLDER = '/var/www/slashml2/data/dataset/text'
UPLOAD_FOLDER = '/Users/lion/Documents/py-workspare/slash-ml/data/dataset/text'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

application = Flask('slashmlapi')

application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

application.debug = True

application.secret_key = os.getenv('SECRET_KEY') or \
'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
application.config['SECRET_KEY'] = application.secret_key

application.config['SESSION_TYPE'] = 'filesystem'

api_session = Session()
api_session.init_app(application)

toolbar = DebugToolbarExtension(application)

#from slashmlapi.controllers import *
#from slashmlapi.controllers import route

@application.route('/getresults', methods=['POST'])
def execute():
    if request.method == 'POST':

        from slashmlapi.controllers.result_controller import ResultController

        result_controller = ResultController(request, **application.config)

        _, info = result_controller.start_operation()

        return json.dumps(info)

    else:
        return 'KO'

if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 8080))
    #application.run('0.0.0.0', port=port)
    application.run(host='0.0.0.0')

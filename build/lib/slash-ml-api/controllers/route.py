# -*- coding: utf-8 -*-
import os
import json
from flask import render_template, request, redirect, session, make_response
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

from api import app


class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])

@app.route('/')
def start():
    return render_template('printer/index.html')

@app.route('/set')
def set():
    session['key'] = 'value'
    resp = make_response('Setting Cookie !')
    resp.set_cookie('framework', 'flask')
    return resp

@app.route('/get')
def get():

    if 'key' in session.__dict__:
        key = session.get('key', 'not set')
        session.pop('key')

    framework = 'NOK'
    if request.cookies.get('framework'):
        framework = request.cookies.get('framework')

    return framework

@app.route('/clear')
def clear():
    resp = make_response('Setting Cookie !')
    resp.set_cookie('framework', '', expires=0)

    return resp

@app.route('/extractfeatures', methods=['GET', 'POST'])
def extract_features():
    """ This function is used to extract features from original text
    """

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            #return redirect(request.url)
            return 'No selected file'

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Call machine learning manager
        from app.ml_manager import MLManager
        # Extract features from give text
        is_success = MLManager.extract_features(filename)
        status = {
            'is_success': is_success
        }

        # Execute Naive Bayes
        return json.dumps(status)

@app.route('/train', methods=['GET', 'POST'])
def train():
    """ This function is used to train model
    """

    #form = CreateForm(request.form)
    if request.method == 'POST':
        
        # Call machine learning manager
        from app.ml_manager import MLManager

        # Extract features from give text
        accuracy = MLManager.train()
        info = {
            'accuracy': accuracy
        }

        # Execute Naive Bayes
        return json.dumps(info)

""" @app.route('/predict', methods=['GET', 'POST'])
def predict():
    
    if request.method == 'POST':
        from slashml.public.test_machinelearning import MachineLearningManager

        # Execute Naive Bayes
        return MachineLearningManager.test() """

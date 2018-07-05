""" Text Classification
Handle the client request, and return prediction results as dictionary to client.
"""

import json
from flask import request

import logging
logfile = '/Users/lion/Documents/py-workspare/slash-ml/logfile.log'

class PredictController(object):
    """ Handle request from client
    """

    def __init__(self, start_time, client_request=request, **kwargs):
        self.kwargs = kwargs
        self.request = client_request
        self.start_time = start_time

        logging.basicConfig(filename=logfile, level=logging.DEBUG)
        logging.info('Prediction controller')


    def start_operation(self):
        """ Execute the command from client
        Start machine learning engine
        Return Accuracy
        """

        # Check input params from client
        error, json_params = self.check_text()

        if not error:
            # Start machine learning here
            from slashmlapp.ml_manager import MLManager

            text = json_params['input_text']
            results = MLManager.classify(self.kwargs, text)
            #logging.info('Predict_Controller: %s' %(json_params))

            return True, results
        else:
            return False, error


    def check_text(self):
        """ Validate the parameters from client's request
        """

        error = {}
        if request.method == 'POST':
            json_params = None
            params = {}
            try:
                # Get params from client request
                params = self.request.form.get('params')
                json_params = json.loads(params)
                # logging.info('Prediction controller %s' %self.request.form)
                # logging.info('Prediction controller %s' %params)
            except ValueError as error:
                error['error'] = 'Input string must be text, not bytes'
                return error, json_params
            else:
                return error, json_params

        else:
            error['error'] = 'Not support method'
            return error, None

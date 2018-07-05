""" 
"""

import os
import json
from flask import request
from werkzeug.utils import secure_filename

import logging
logfile = '/Users/lion/Documents/py-workspare/slash-ml/logfile.log'

class ResultController(object):
    """ Handle request from client
    """

    def __init__(self, start_time, client_request=request, **kwargs):
        self.kwargs = kwargs
        self.request = client_request
        self.start_time = start_time

        logging.basicConfig(filename=logfile, level=logging.DEBUG)
        logging.info('Result controller')

    def start_operation(self):
        """ Execute the command from client
        Start machine learning engine
        Return Accuracy
        """

        # Check file
        is_good_file, info = self.check_file()

        if is_good_file:
            # Check input params from client
            is_error, json_params = self.check_text()

            if bool(is_error):
                return is_error, json_params
            else:
                # Start machine learning here
                from slashmlapp.ml_manager import MLManager

                # Path to zip file
                path_textfile = info['filename']
                results = MLManager.get_results(path_textfile, json_params, '', self.start_time)
                return True, results
        else:
            return is_good_file, info


    def check_file(self):
        """ Check the validity of file sent from client side
        """

        # File manipulation status
        status = {}

        # check if the post request has the file part
        if 'datasource' not in self.request.files:
            status['error'] = 'No file part'
            return False, status

        file = request.files['datasource']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            #return redirect(request.url)
            status['error'] = 'No selected file'
            return False, status

        # Get filename
        # Save to local hardrive
        filename = secure_filename(file.filename)
        # file.save(os.path.join(self.kwargs['UPLOAD_FOLDER'], filename))
        is_saved, error = self.save_file(self.kwargs['UPLOAD_FOLDER'], filename, file)

        if is_saved:

            # Return filename
            status['filename'] = filename
            return True, status
        else:

            # Return error if something wrong
            status['error'] = error
            return False, status


    def save_file(self, path_to_dir, filename, file_object=request.files):
        """ Save file sent from client to local hardrive
        """

        ## check if a file exists on disk ##
        ## if exists, delete it else show message on screen ##
        if os.path.exists(path_to_dir):
            try:
                file_object.save(os.path.join(path_to_dir, filename))
            except IOError as error:
                err_message = "%s and %s" % (error.filename, error.strerror)
                return False, err_message
            else:
                return True, None
        else:
            return False, None


    def check_text(self):
        """ Validate the parameters from client's request
        """
        logging.info('In check text: check_text')

        info = {}
        if request.method == 'POST':
            #json_params = None
            params = {}
            try:
                logging.info('Res controller %s' %params)
                # Read parameters from client
                cparams = self.request.form.to_dict(flat=True)
                #cparams = {'params[algo][0]': 'NB', 'params[algo][1]': 'NN', 'params[eval_setting]': 'loo', 'params[PR][method]': 'doc_freq', 'params[PR][threshold]': '25', 'params[NN][hidden_layer_sizes][0]': '20', 'params[NN][hidden_layer_sizes][1]': '56', 'params[NN][learning_rate]': '0.012', 'params[NN][momentum]': '0.5', 'params[NN][random_state]': '0', 'params[NN][max_iter]': '200', 'params[NN][activation]': 'tanh', 'params[DT][criterion]': 'gini', 'params[DT][max_depth]': '30', 'params[DT][min_criterion]': '0.05'}
                logging.info('Res controller cparams %s' %cparams)    
                # # Temp set params
                # # params['algo'] = ['NB', 'NN', 'DT']
                # # params['eval_setting'] = 'loo'
                # # params['PR'] = {'method': 'doc_freq', 'threshold': 25}
                # # params['DT'] = {'criterion': 'gini', 'max_depth': 25, 'min_criterion': 0.05}
                # # params['NN'] = {'hidden_layer_sizes': (250, 100), 'learning_rate': 0.012,\
                # #  'momentum': 0.5, 'random_state':0, 'max_iter':200, 'activation': 'tanh'}
                params['algo'] = [cparams['params[algo][0]'], cparams['params[algo][1]'], 'DT']
                params['eval_setting'] = cparams['params[eval_setting]']
                params['PR'] = {'method': cparams['params[PR][method]'], 'threshold': int(cparams['params[PR][threshold]'])}
                params['DT'] = {'criterion': cparams['params[DT][criterion]'],\
                'max_depth': int(cparams['params[DT][max_depth]']), 'min_criterion': float(cparams['params[DT][min_criterion]'])}

                # Manipulate hidden layer in tuple
                h_layer_sizes = tuple(int(x) for x in cparams['params[NN][hidden_layer_sizes]'].split(',') if x.strip())

                params['NN'] = {'hidden_layer_sizes': h_layer_sizes, 'learning_rate': float(cparams['params[NN][learning_rate]']),\
                'momentum': float(cparams['params[NN][momentum]']), 'random_state':int(cparams['params[NN][random_state]']),\
                'max_iter':int(cparams['params[NN][max_iter]']), 'activation': cparams['params[NN][activation]']}

                logging.info('Res controller %s' %params)
            except ValueError:
                info['error'] = 'Input string must be text, not bytes'
            else:
                return info, params
        else:
            info['error'] = 'Not support method'
            return info, None

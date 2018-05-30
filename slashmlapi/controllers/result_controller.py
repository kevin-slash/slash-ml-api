""" 
"""

import os
import json
from flask import request
from werkzeug.utils import secure_filename


class ResultController(object):
    """ Handle request from client
    """

    ''' def __init__(self, client_request=request, **kwargs):
        self.kwargs = kwargs
        self.request = client_request '''

    def __init__(self, start_time, client_request=request, **kwargs):
        self.kwargs = kwargs
        self.request = client_request
        self.start_time = start_time


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

                #path_textfile = 'data.zip'
                #list_algo = ['NB', 'NN']
                path_textfile = info['filename']
                list_algo = json_params['algo']

                #results = MLManager.get_results(path_textfile, list_algo, '')

                #logging.info('Start ML')
                #print('Start ML')
                #results = MLManager.get_results(path_textfile, list_algo, '')
                results = MLManager.get_results(path_textfile, list_algo, '', self.start_time)

                #print('End ML')

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
        #file.save(os.path.join(self.kwargs['UPLOAD_FOLDER'], filename))
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

        info = {}
        if request.method == 'POST':

            json_params = None
            params = {}
            try:

                # Temp set params
                params['algo'] = ['NB', 'NN']
                params['eval_setting'] = 'loo'

                # Get params from client request
                #params = self.request.form.get('params')
                #json_params = json.loads(params)
                json_params = params
            except ValueError:
                info['error'] = 'Input string must be text, not bytes'
            else:
                return info, json_params
        else:
            info['error'] = 'Not support method'
            return info, None

if __name__ == "__main__":
    
    result_controller = ResultController()
    _info, _params = result_controller.check_text()
    print(_info)
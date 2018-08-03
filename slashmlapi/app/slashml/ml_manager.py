""" This is test machine learning class
"""

import sys, os
import argparse
import time
import numpy as np

from khmerml.machine_learning import MachineLearning
from khmerml.preprocessing.preprocessing_data import Preprocessing
from khmerml.utils.file_util import FileUtil
from khmerml.utils.bg_colors import Bgcolors

import logging

class MLManager(object):
  """
    Machine learning application built on top of slashml
  """

  @staticmethod
  def perform_algo(ml, algo, dataset):
    result_acc = []
    result_acc_train = []
    result_exec_time = []
    for i in range(10):
      exec_st = time.time()
      # split dataset -> train set, test set
      training_set, test_set = ml.split_dataset(dataset, 1)
      # train
      model = algo.train(training_set)
      # make a prediction
      pred_test = algo.predict(model, test_set)
      pred_train = algo.predict(model, training_set)

      # Prediction accuracy
      acc = ml.accuracy(pred_test, test_set)
      acc_train = ml.accuracy(pred_train, training_set)
      exec_time = time.time() - exec_st
      print(acc, acc_train, exec_time)
      result_acc.append(acc)
      result_acc_train.append(acc_train)
      result_exec_time.append(exec_time)

    mean_acc = np.mean(np.array(result_acc))
    mean_acc_train = np.mean(np.array(result_acc_train))
    mean_exec_time = np.mean(np.array(result_exec_time))

    return {
      'acc': round(mean_acc, 2),
      'acc_train': round(mean_acc_train, 2),
      'exec_time': round(mean_exec_time, 2)
    }

  @staticmethod
  def get_results(path_textfile, params, config, start_time):
    """
      This function performs features extraction from client's data source\
      Train model based on extracted features
      Get Accuracy of each algorithm (e.g: Naive Bayes, Neural Network) based on\
      evaluation criteria e.g: LOO, 5 folds or 10 folds
    """

    # Store config for next use
    config = config
    is_unicode = config.get('is_unicode', None)
    config['is_unicode'] = 'true' if is_unicode != None else False
    #logfile = '/Users/lion/Documents/py-workspare/slash-ml/logfile.log'
    #logging.basicConfig(filename=logfile, level=logging.DEBUG)
    config['passion'] = "passion"
    # Perform features extraction
    is_successful_fextract = MLManager.extract_features(path_textfile, config)
    #is_successful_fextract = True

    if is_successful_fextract:
      whole_st = time.time()

      prepro = Preprocessing(**config)

      # preposessing
      params_prepro = params['PR']

      dataset_matrix = prepro.loading_data(config['text_dir'], params_prepro['method'],\
       'all', params_prepro['threshold'])

      # Remove sub-directory from "data/dataset/text"
      FileUtil.remove_file(config['text_dir'], ignore_errors=True)

      #load dataset from file (feature data)
      filename = "doc_freq_" + str(params_prepro['threshold']) + ".csv"
      dataset_path = FileUtil.dataset_path(config, filename)
      dataset_sample = FileUtil.load_csv(dataset_path)

      prepro_time = time.time() - whole_st

      ml = MachineLearning(**config)

      # choose your algorithm
      nb_algo = ml.NiaveBayes()

      params_nn = params['NN']
      nn_algo = ml.NeuralNetwork(hidden_layer_sizes=params_nn['hidden_layer_sizes'],\
       learning_rate=params_nn['learning_rate'], momentum=params_nn['momentum'],\
        random_state=params_nn['random_state'], max_iter=params_nn['max_iter'],\
         activation=params_nn['activation'])

      params_dt = params['DT']
      dt_algo = ml.DecisionTree(criterion=params_dt['criterion'], prune='depth',\
       max_depth=params_dt['max_depth'], min_criterion=params_dt['min_criterion'])

      nb_result = MLManager.perform_algo(ml, nb_algo, dataset_sample)
      nn_result = MLManager.perform_algo(ml, nn_algo, dataset_sample)
      dt_result = MLManager.perform_algo(ml, dt_algo, dataset_sample)

      print(nb_result, nn_result, dt_result)

      total_execution_time = time.time() - whole_st

      result = {
        'com_time': round(total_execution_time, 2),
        'text_extract_time': round(prepro_time, 2),
        'figure_on_testing_data': {
          'NB': nb_result['acc'],
          'NN': nn_result['acc'],
          'DT': dt_result['acc'],
        },
        'figure_on_training_data': {
          'NB': nb_result['acc_train'],
          'NN': nn_result['acc_train'],
          'DT': dt_result['acc_train'],
        },
        'on_testing_data': {
          'NB': {'accuracy': nb_result['acc'], 'time': nb_result['exec_time']},
          'NN': {'accuracy': nn_result['acc'], 'time': nn_result['exec_time']},
          'DT': {'accuracy': dt_result['acc'], 'time': dt_result['exec_time']},
        },
        'on_training_data': {
          'NB': {'accuracy': nb_result['acc_train'], 'time': nb_result['exec_time']},
          'NN': {'accuracy': nn_result['acc_train'], 'time': nn_result['exec_time']},
          'DT': {'accuracy': dt_result['acc_train'], 'time': dt_result['exec_time']},
        }
      }

    return result


  @staticmethod
  def classify(config, text):
    """ Text classification
    """

    # Preprocess: transform text to frequency
    prepro = Preprocessing(**config)
    mat = prepro.loading_single_doc(text, 'doc_freq', config['threshold'])
    # Initialize only 3 algorithms at the moment
    ml = MachineLearning(**config)

    # Perform prediction
    # Naive Bayes
    nb_algo = ml.NiaveBayes()
    nb_model = nb_algo.load_model()
    nb_prediction = nb_algo.predict(nb_model, [mat])

    # ANN
    nn_algo = ml.NeuralNetwork(hidden_layer_sizes=(250, 100),\
     learning_rate=0.012, momentum=0.5, random_state=0, max_iter=200, activation='tanh')
    nn_model = nn_algo.load_model()
    nn_prediction = nn_algo.predict(nn_model, [mat])

    # DT
    dt_algo = ml.DecisionTree(criterion='gini', prune='depth', max_depth=30, min_criterion=0.05)
    dt_model = dt_algo.load_model()

    #norm_mat = prepro.normalize_dataset(np.array([mat])) # use with decision tree only
    #norm_mat = prepro.normalize_dataset(np.array([mat])) # use with decision tree only
    #dt_prediction = dt_algo.predict(dt_model, norm_mat)
    dt_prediction = dt_algo.predict(dt_model, np.array([mat]))

    # Get the best labe outputed by BN, NN, DT
    nb_label = ml.to_label(nb_prediction, config['label_match'])
    nn_label = ml.to_label(nn_prediction, config['label_match'])
    dt_label = ml.to_label(dt_prediction, config['label_match'])

    # Prepare results of:
    # (1) Naive Bayes (2) Neural Network (3) Decision Tree
    result = {
      'NB': nb_label,
      'NN': nn_label,
      'DT': dt_label
    }

    return result


  @staticmethod
  def extract_features(text_file, config):
    """ this function can be used to extract features \
    in a format supported by machine learning \
    algorithms from datasets consisting of formats such as text.
    """

    #config = MLManager.config
    #path_to_zipfile = FileUtil.path_to_file(config, config['text_dir'], text_file)
    #path_to_tempdir = FileUtil.path_to_file(config, config['archive_dir'], text_file)
    path_to_zipfile = FileUtil.path_to_file(config['text_dir'], text_file)
    path_to_tempdir = FileUtil.path_to_file(config['archive_dir'], text_file)

    if os.path.exists(path_to_zipfile) is False:
        # Move data.zip file to temp directory
        FileUtil.move_file(path_to_tempdir, path_to_zipfile)
    try:
        # Extract zip file
        FileUtil.extract_zipfile(path_to_zipfile, FileUtil.join_path(config['text_dir']))
        # Move data.zip file to temp directory
        FileUtil.move_file(path_to_zipfile, path_to_tempdir)
    except OSError as error:
      raise Exception(error)
    else:
      return True


  @staticmethod
  def test_train_model():
    """ this function can be used to extract features \
    in a format supported by machine learning \
    algorithms from datasets consisting of formats such as text.
    """

    _path_textfile = 'chatbot.zip'
    _list_algo = ""
    start_time = time.time()
    results = MLManager.get_results(_path_textfile, _list_algo, '', start_time)

    print('accuracy %s' %(results))


  @staticmethod
  def test_prediction():
    """ Start predicting
    """

    # Basic configuration
    config = {
      'text_dir': 'data/dataset/chatbot',
      'dataset': 'data/matrix',
      'bag_of_words': 'data/bag_of_words',
      'train_model': 'data/model/train.model',
    }

    #text = 'sorry i don\'t understand what you are saying, tell me more!'
    text = 'How are you.'
    expected_result = MLManager.classify(config, text)
    print('Output', expected_result)


if __name__ == "__main__":

  # Train model
  MLManager.test_train_model()

  # Test input text
  #MLManager.test_prediction()

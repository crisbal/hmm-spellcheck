# HMM Corrector

Cristian Baldi - Simone Vitali

## How to install

* `git clone` this repo
* `pip install -r requirements.txt`

## Testing the correction model

* `python correct.py` for command line usage
* `python web_interface.py` for a web bases interface

## Building a new model

* Create a folder inside `data/` and name it whatever you want
* Add some `.txt` files to it
* Change the current model in `config.py`
* Run `python learn.py` and `python build_model.py`
* You can now use it.

## Running performance tests

* `python test.py`

## Files and folders

* `data/`, data for building the model and running the correction alghoritm
* `web_interface`, files for the web interface
*  `build_model.py`, build the required objects for running the model
*  `build_test_set.py`, build the test set for running tests
*  `config.py`, configuration file
*  `correct.py`, command line interface
*  `learn.py`, analyze the text and build word distributions and transitions probability
*  `probabilistic_distance.py`, compute the probabilistic distance between two strings
*  `test.py`, run tests
*  `Viterbi.py`, implements the viterbi algorithm and state selection functions
*  `web_interface.py`, runs the web interface



## Raw Dataset

https:// datacloud [DOT] di.unito [DOT] it/index.php/s/Wn8tRFyETxZkqJc

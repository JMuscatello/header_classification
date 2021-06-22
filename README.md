# header_classification

## Overview

For this task I have outlined my approach in the jupyter notebook `test.ipynb`. Here I have used two approaches, the first being a simple heuristic approach
using regular expressions and optional other logic and the second a machine learning approach where I have trained a logistic regression classifier using the
html file supplied with the test.

I have not gone into too much detail regarding model evaluation since the data is only from one document, and the performance is therefore
expected to be poor. However I have made an attempt at trying to optimise the paramters of the model.

To illustrate a potential way to use the model in production, I have created a Flask web app to serve the model, as well as a training script to create the model.

## Installation

Set up the relevant virtual environment and install dependencies.

Initialise and activate the virtual environment:

```shell
python3 -m venv venv
. venv/bin/activate
```

pip install from requirements file:

```
pip install -r requirements.txt
```
## Running the training script

The training script is used to generate a model for use in the Flask application. It takes two arguments, one is the path to the html file 
and the other is the path to the resultant model, e.g.
```
./train_model.py --path_to_data ./document-headers/files/nda_titles_highlighted.html --path_to_output ./app/model.pkl

```

This will produce a model and display information.

## Running the Flask app
Go to the `app/` directory
```
cd ./app
```
Flask will be install via pip from the requirements file. Flask requires the app name as a environment variable.
```
export FLASK_APP=header_classifier
```
The app also requires the path to the model produced by the trainign script, which is supplied as an evnironment variable, e.g:
```
export PATH_TO_MODEL=./model.pkl
```
Next start the app. The app will run by default on `localhost:5000`.
```
flask run
```
The app should be ready to accept requests if the model loads correctly. The app contains swagger documentation detailing the api found at `localhost:5000/api/v1/`.
Currently the app only has one endpoint at `/api/v1/classifier/predict` which will run the model on data in the json format given in the test when
sent a `POST` request with the given json body. An example `curl` command is shown below:
```shell
curl -X POST \
  http://127.0.0.1:5000/api/v1/classifier/predict \
  -H 'Content-Type: application/json' \

  -H 'cache-control: no-cache' \
  -d '{"paragraphs": [
	{
		"p_id": 0,
		"p_text": "NON-DISCLOSURE AGREEMENT",
		"p_start_offset": 0
	},
	{
		"p_id": 1,
		"p_text": "This Non-Disclosure Agreement (the “Agreement”) is made on 9 January 2014 (“Effective Date”).",
		"p_start_offset": 24
	}
]}'
```
with a json response
```json
{
    "header_ids": [
        0
    ]
}
```

Corresponding to the `p_id`s of the positively clasified paragraphs.

## Limitations

For this test I did not implement a system that applied a complex logic to the problem (for example a set of heuristics expressed as a decision tree),
as I wanted to concentrate on a potential ML approach. In reality there will probably be quite a few heuristics that will be applied as either pre or post
processing steps to the actual classification. The ML side could also be much more complex, and involve various other data preprocessing steps 
and feature extraction methods. It would also make sense to take into account the sequence of paragraphs, as it is unlikely that two headers will follow in
succession for example. Overall there are many ways such a system could be improved, but this was not possible to explore due to time constraints.





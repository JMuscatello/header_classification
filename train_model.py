#!/usr/bin/env python
"""
Short script to reproduce logic found in notebook for training model for use
with flask webapp
"""

import argparse
import re
import pickle

from pathlib import Path

from bs4 import BeautifulSoup

from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


def get_paragraphs_text_labels(html_file):
    """
    Returns processed text and labels from html file, using beautiful soup

    Args:
        html_file: string containing html

    Returns:
        list of paragraph text, list of labels (1 for header, 0 otherwise)
    """

    soup = BeautifulSoup(html_file, 'html.parser')

    docs = []
    labels = []

    for p in soup.find_all('p'):
        text = p.get_text()
        if text.lower().islower():
            docs.append(preprocess(p.get_text()))
            if 'background-color: orange' in p['style']:
                labels.append(1)
            else:
                labels.append(0)

    return docs, labels


def preprocess(text):
    """
    Preprocesses text to replace header numbers and indicate all caps by
    appending a string

    Args:
        text (String): String to apply preprocessing to

    Returns:
        processed string
    """
    text = re.sub(r'[0-9]+(\.?)\s+(?=[A-Z].+)', 'NUM', text)
    if text.isupper():
        text + ' ALL_CAPS'
    return text


def main():
    parser = argparse.ArgumentParser(
        description='A script to train a header classifier using html data')

    parser.add_argument(
        '-i',
        '--path_to_data',
        type=str,
        required=True,
        help='Path to html file'
    )
    parser.add_argument(
        '-o',
        '--path_to_output',
        type=str,
        required=True,
        help='path to model output'
    )

    args = parser.parse_args()

    path_to_data = Path(args.path_to_data)
    path_to_output = Path(args.path_to_output)

    with path_to_data.open('r') as f_in:
        html_file = f_in.read()

    X, y = get_paragraphs_text_labels(html_file)    
    print(f'There are {len(X)} paragraphs.')

    clf = Pipeline([
        (
            'tfidf',
            TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95
            )
        ),
        (
            'lr',
            LogisticRegression(
                class_weight='balanced',
                C=1.0
            )
        )
    ])

    params = {
        'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
        'tfidf__stop_words': [None, 'english'],
        'tfidf__min_df': [1, 5],
        'lr__C': [0.1, 1.0, 10.0],
        'lr__class_weight': ['balanced', None]
    }

    gs_lr = GridSearchCV(
        estimator=clf,
        param_grid=params,
        scoring='f1',
        n_jobs=8,
        cv=5,
        verbose=5
    )

    print('Optimising model...')

    gs_lr.fit(X, y)
    print(f'Found best params: {gs_lr.best_params_}')
    print(f'with average f1 score: {gs_lr.best_score_}')

    print(f'Saving model to {str(path_to_output)}')

    with path_to_output.open('wb') as f_out:
        pickle.dump(gs_lr.best_estimator_, f_out)


if __name__ == '__main__':
    main()

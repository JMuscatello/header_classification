import os


class Config:
    """
    Configuration for Flask app
    """
    PATH_TO_MODEL = os.environ.get('PATH_TO_MODEL', './model.pkl')

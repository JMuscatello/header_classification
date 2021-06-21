from pathlib import Path
import pickle

from flask import Flask
from flask.cli import FlaskGroup

from header_classifier.api import blueprint as api_blueprint

from config import Config


PKG_NAME = Path(__file__).parent.name

print(PKG_NAME)

def create_app(app_name=PKG_NAME, config_class=Config):

    app = Flask(app_name)

    app.config.from_object(config_class)
    # Load model into config
    print('Loading model...')
    print(app.config['PATH_TO_MODEL'])
    with open(app.config['PATH_TO_MODEL'], 'rb') as f_in:
        app.config['model'] = pickle.load(f_in)
    print('Done.')

    app.register_blueprint(api_blueprint, url_prefix='/api/v1/')

    return app


def run_cli():
    app = create_app()

    cli = FlaskGroup(create_app=lambda: app)

    cli()

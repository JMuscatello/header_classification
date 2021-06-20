from flask import Blueprint
from flask_restx import Api

from .classification import api as classification_api

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Header Classification App',
    version='0.1',
    description='API for identifying headers'
)

api.add_namespace(classification_api, path='/classifier')

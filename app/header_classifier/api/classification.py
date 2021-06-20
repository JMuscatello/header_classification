from flask import current_app as app
from flask import jsonify

from flask_restx import Namespace, Resource, fields


api = Namespace(
    'classifier',
    description='Classify mentions according to several categories'
)

paragraph_model = api.model(
    'Model for paragraph data',
    {
        'p_id': fields.Integer(description='paragraph id'),
        'p_text': fields.String(description='paragraph text'),
        'p_start_offset': fields.Integer(description='paragraph offset')
    }
)

paragraph_list_model = api.model(
    'Paragraph list model',
    {
        'paragraphs': fields.List(fields.Nested(paragraph_model))
    }
)

@api.route('/predict')
class Predict(Resource):

    @api.expect(paragraph_list_model, validate=False)
    @api.doc(description='Predict header from list of paragraphs')
    def post(self):

        paragraphs = api.payload['paragraphs']
        results = predict(paragraphs)

        return jsonify({'results': results})

def predict(paragraphs):
    return "blah blah"

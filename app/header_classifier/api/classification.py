from flask import current_app as app
from flask import jsonify

from flask_restx import Namespace, Resource, fields

from ..lib.preprocessing import preprocess

api = Namespace(
    'classifier',
    description='Classify mentions according to several categories'
)

paragraph_model = api.model(
    'Paragraph data',
    {
        'p_id': fields.Integer(description='paragraph id'),
        'p_text': fields.String(description='paragraph text'),
        'p_start_offset': fields.Integer(description='paragraph offset')
    }
)

paragraph_list_model = api.model(
    'Paragraph list',
    {
        'paragraphs': fields.List(fields.Nested(paragraph_model))
    }
)

header_ids_model = api.model(
    'Header ids',
    {
        'header_ids': fields.List(fields.Integer(
            description='p_ids corresponding to headers'))
    }
)

@api.route('/predict')
class Predict(Resource):

    @api.expect(paragraph_list_model, validate=False)
    @api.doc(description='Predict header from list of paragraphs')
    @api.marshal_with(header_ids_model) 
    def post(self):

        paragraphs = api.payload['paragraphs']
        results = predict(paragraphs)

        return {'header_ids': results}


def predict(paragraphs):
    """
    Use loaded model to predict on a list of paragraph objects.

    Args:
        paragraphs: List of dictionaries of form
            {
                'p_id': <int>,
                'p_text': <str>,
                'p_start_offset': <int>
            }
    Returns:
        list of p_ids corresponding to positive predictions
    """
    header_index_list = []
    docs = [preprocess(p['p_text']) for p in paragraphs]
    predictions = app.config['model'].predict(docs)

    for pred, paragraph in zip(predictions, paragraphs):
        if pred:
            header_index_list.append(paragraph['p_id'])

    return header_index_list

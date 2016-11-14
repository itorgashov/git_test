from flask import Flask, jsonify, abort, make_response, request, Response, current_app
from flask_cors import CORS, cross_origin
from datetime import timedelta
from functools import update_wrapper


app = Flask(__name__)
CORS(app)

drinks = [
    {
        'id': 1,
        'name': u'Ardbeg',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': 10
    },	
    {
        'id': 2,
        'name': u'Ardbeg 1990 Cask',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': None
    },
    {
        'id': 3,
        'name': u'Bowmore Islay ',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': 12
    },	
    {
        'id': 4,
        'name': u'Bowmore Sherry Cask',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': 16
    },	
    {
        'id': 5,
        'name': u'Bowmore Islay',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': 25
    },	
    {
        'id': 6,
        'name': u'Bruichladdich',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': 15
    },	
    {
        'id': 7,
        'name': u'Lagavulin 16 yr',
        'country': u'Scotland',
        'region': None, 
        'age': 16
    },	
    {
        'id': 8,
        'name': u'Lagavulin Distillers Edition',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': None
    },
    {
        'id': 9,
        'name': u'Laphroaig',
        'country': u'Scotland',
        'region': u'Islay', 
        'age': 15
    },	
    {
        'id': 10,
        'name': u'Glenmorangie',
        'country': u'Scotland',
        'region': u'Northern Highland', 
        'age': 15
    },
    {
        'id': 11,
        'name': u'Oban (Western)',
        'country': u'Scotland',
        'region': u'Northern Highland', 
        'age': 14
    },	
    {
        'id': 12,
        'name': u'The Dalmore',
        'country': u'Scotland',
        'region': u'Northern Highland', 
        'age': 12
    },	
    {
        'id': 13,
        'name': u'Auchentoshan',
        'country': u'Scotland',
        'region': u'Lowland', 
        'age': 10
    },	
    {
        'id': 14,
        'name': u'The Balvenie Portwood',
        'country': u'Scotland',
        'region': u'Speyside', 
        'age': 21
    },	
    {
        'id': 15,
        'name': u'The Macallan Fine Oak',
        'country': u'Scotland',
        'region': u'Speyside', 
        'age': 10
    },	
    {
        'id': 16,
        'name': u'Redbreast',
        'country': u'Ireland',
        'region': None, 
        'age': 12
    },		
]



@app.route('/todo/api/v1.0/drinks', methods=['GET'])
def get_drinks():	
    filter_name = request.args.get('name')
    filter_country = request.args.get('country')
    filter_region = request.args.get('region')
    filter_age = request.args.get('age')
    filtered_drinks = filter(lambda d: ((filter_name is None or len(filter_name) == 0 or d['name'].lower() == filter_name.lower()) and  \
        (filter_country is None or len(filter_country) == 0 or d['country'].lower() == filter_country.lower()) and \
        (filter_region is None or len(filter_region) == 0 or d['region'].lower() == filter_region.lower()) and \
        (filter_age is None or len(filter_age) == 0 or d['age'] == safe_cast(filter_age, int, None))), drinks)
    resp = make_response(jsonify({'drinks': filtered_drinks}))
    resp.headers['Access-Control-Allow-Origin'] = '*'	
    return resp

@app.route('/todo/api/v1.0/drinks/<int:drink_id>', methods=['GET'])
def get_drink(drink_id):
    drink = filter(lambda d: d['id'] == drink_id, drinks)
    if len(drink) == 0:
        abort(404)
    return jsonify({'drink': drink[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found!!!'}), 404)	
	
@app.route('/todo/api/v1.0/drinks', methods=['POST'])
def create_drink():
    if not request.json or not 'name' in request.json:
        abort(400)
    drink = {
		'id': drinks[-1]['id'] + 1,
        'name': request.json.get('name'),
        'country': request.json['country'],
        'region': request.json['region'],
        'age': int(request.json.get('age', "")),
    }
    drinks.append(drink)
    return jsonify({'drink': drink}), 201	
	
@app.route('/todo/api/v1.0/drinks/<int:drink_id>', methods=['PUT'])
def update_drink(drink_id):
    drink = filter(lambda d: d['id'] == drink_id, drinks)
    if len(drink) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not unicode:
        abort(400)
    if 'country' in request.json and type(request.json['country']) is not unicode:
        abort(400)
    if 'region' in request.json and type(request.json['region']) is not unicode:
        abort(400)
    if 'age' in request.json and type(request.json['age']) is not int:
        abort(400)
    drink[0]['name'] = request.json.get('name', drink[0]['name'])		
    drink[0]['country'] = request.json.get('country', drink[0]['country'])
    drink[0]['region'] = request.json.get('region', drink[0]['region'])
    drink[0]['age'] = request.json.get('age', drink[0]['age'])
    return jsonify({'drink': drink[0]})

@app.route('/todo/api/v1.0/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink = filter(lambda d: d['id'] == drink_id, drinks)
    if len(drink) == 0:
        abort(404)
    drinks.remove(drink[0])
    resp = make_response(jsonify({'drinks': drinks}))
    resp.headers['Access-Control-Allow-Origin'] = '*'	
    return resp	
	
def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default
	
if __name__ == '__main__':
    app.run(debug=True)
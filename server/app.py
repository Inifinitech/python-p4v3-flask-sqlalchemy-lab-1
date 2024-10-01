# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        return jsonify({
            'id': earthquake.id, 
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year

        })
    else:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquake_magnitude(magnitude):
    earthmags = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    earthquakeMag_list = [{
        'id': earthmag.id,
        'location': earthmag.location,
        'magnitude': earthmag.magnitude, 
        'year': earthmag.year
    } for earthmag in earthmags]

    return jsonify({
        'count': len(earthquakeMag_list),
        'quakes': earthquakeMag_list
    })
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)

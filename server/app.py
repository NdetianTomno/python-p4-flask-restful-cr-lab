#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        title = "Plants Page"
        plants = Plant.query.all()
        serialized_plants = [plant.serialize() for plant in plants]
        return jsonify(title=title, plants=serialized_plants)

    def post(self):
        data = request.get_json()
        plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(plant)
        db.session.commit()
        return jsonify(plant), 201


class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            return jsonify(plant)
        else:
            return make_response(jsonify(error='Plant not found'), 404)


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

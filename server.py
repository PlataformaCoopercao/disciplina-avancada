from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from maps import random_hillclimbing_final
from settings import API_KEY
# from nodes import Node, random_hillclimbing_final

app = Flask(__name__)
api = Api(app)


class Optimizer(Resource):
    def get(self):
        return

    def put(self):
        data = request.form['route']
        list_route = data[1:-1].split(',')
        route = list_route
        new_route = random_hillclimbing_final(route, opt_limit=3, key=API_KEY)
        return jsonify(route=str(new_route))


api.add_resource(Optimizer, '/')

if __name__ == '__main__':
    app.run(debug=True)

# put('http://localhost:5000/', data={'route': '[48 99, 16 32, 21 74, 40 9]'}).json()
# put('http://localhost:5000/', data={'route': "[place_id:EjFQcmHDp2EgUmlvIEJyYW5jbyAtIFJlY2lmZSwgUEUsIDUyMTcxLTAxMSwgQnJhemlsIi4qLAoUChIJPRgmj6QYqwcRjfmoe7K_nmoSFAoSCV-IZaWiGKsHEbeEm1dSDiuA,place_id:ChIJZVvB3KYfqwcR-T7Po_gXFgY,place_id:ChIJlTXqY8kfqwcRD-si4uv7Sc4]"}).json()

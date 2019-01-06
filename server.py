from flask import Flask, request
from flask_restful import Resource, Api
from nodes import Node, random_hillclimbing_final

app = Flask(__name__)
api = Api(app)

todos = {}


class Optimizer(Resource):
    def get(self):
        return {todo_id: todos[todo_id]}

    def put(self):
        data = request.form['route']
        list_route = list(data[1:-1].split(','))
        route = [Node(*node.strip().split()) for node in list_route]
        new_route = random_hillclimbing_final(route, opt_limit=18)
        # route = [Node(node.strip().split()) for node in list(route[1::1].split(','))]
        # print(route)
        # route = [Node(node) for node in route]
        return str(new_route)


api.add_resource(Optimizer, '/')

if __name__ == '__main__':
    app.run(debug=True)

# put('http://localhost:5000/',
#     data={'route': '[48 99, 16 32, 21 74, 40 9]'}).json()

from flask import Flask
from flask_restx import Api, Resource, Namespace

app = Flask(__name__)
api = Api(app, version='1.0', title='Podcast API',
    description='API de prueba para subir podcasts',
)

ns = Namespace('users', description='Operaciones get y post para los usuarios')

api.add_namespace(ns)

@ns.route('/<id>')
@ns.doc(params={'id': 'ID usuario'})
class Users(Resource):
    def get(self, id):
        return {}

    def post(self, id):
        api.abort(403)


if __name__ == '__main__':
    app.run(debug=True)
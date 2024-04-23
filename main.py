from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse

app = Flask(__name__, static_url_path='', static_folder='frontend')
api = Api(app)

donors = {
    1: {"name": "Averkin M.E.", "10.11.2003": 15},
    2: {"name": "Averin T.O.", "17.19.2003": 10}
}


class DonorList(Resource):
    def get(self):
        return {"donors": donors}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Name cannot be blank")
        parser.add_argument("blood_type", type=str, required=True, help="Blood type cannot be blank")
        args = parser.parse_args()
        donor = {"name": args["name"], "blood_type": args["blood_type"]}
        donors[len(donors) + 1] = donor
        return donor, 201


api.add_resource(DonorList, "/api/donors")


@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)

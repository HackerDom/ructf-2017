from flask import Flask, request, abort, jsonify
from flask_restful import reqparse, Resource


app = Flask(__name__)


@app.route("/api/register", methods=["POST"])
def registration():
    return "It will be here, a few commits later..."


class OrganisationInfoApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title')


app.run(host="0.0.0.0", port=8080)

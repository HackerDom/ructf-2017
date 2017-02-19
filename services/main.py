from flask import Flask, request, abort


app = Flask(__name__)


@app.route("/api/register", methods=["POST"])
def registration():
    return "It will be here, a few commits later..."


app.run(host="0.0.0.0", port=8080)
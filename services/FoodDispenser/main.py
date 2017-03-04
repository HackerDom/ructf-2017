from flask import Flask, request, jsonify
from json import loads, JSONDecodeError
from rest import rest_hub

app = Flask(__name__)


@app.route("/api/v1/<user_type>/<action>", methods=["POST"])
def registration(user_type, action):
    json_object = get_request_json()
    if json_object:
        return jsonify({"response": rest_hub.rest_handler.handle_action(
            user_type, action, json_object)})
    else:
        return jsonify({"response": {"error": "Received incorrect data!"}})


def get_request_json():
    try:
        return loads(request.data)
    except JSONDecodeError:
        return None
    except ValueError:
        return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

from flask import Flask, request, jsonify
#from uwsgidecorators import cron
from json import loads, JSONDecodeError
from api import api_hub

app = Flask(__name__)


@app.route("/api/v1/<user_type>/<action>", methods=["POST"])
def registration(user_type, action):
    json_object = get_request_json()
    if json_object:
        return jsonify({"response": api_hub.api_handler.handle_action(
            user_type, action, json_object)})
    else:
        return jsonify({"response": {"error": "Received incorrect data!"}})


#@cron(-1, -1, -1, -1, -1)
#def dynamically_load_config_changes(_):
#    __config.update_config()


def get_request_json():
    try:
        return loads(request.data.decode())
    except UnicodeDecodeError:
        return None
    except JSONDecodeError:
        return None
    except ValueError:
        return None
    except TypeError:
        return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

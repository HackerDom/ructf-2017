from flask import Flask, request, jsonify, render_template, redirect
#from uwsgidecorators import cron
from json import loads, JSONDecodeError
from api import api_hub
from database.requests import tokenizer, user_requests, rating_requests


app = Flask(__name__, static_folder='static', static_url_path='')


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


def check_cookie():
    cookie = request.cookies.get("token")
    try:
        user_id, username = tokenizer.verify_token(cookie)
        return user_id, username
    except ValueError:
        return None


@app.route("/")
def main_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_page():
    login = request.form["login"]
    password = request.form["password"]
    try:
        user_id, username, is_food = user_requests.check_user_password(login, password)
        if not is_food:
            raise ValueError()
        token = tokenizer.generate_token(user_id, username, is_food)
        response = app.make_response(redirect("cabinet"))
        response.set_cookie("token", token)
        return response
    except ValueError:
        return redirect("/#badlogin")


@app.route("/cabinet")
def cabinet_page():
    user_tuple = check_cookie()
    if not user_tuple:
        return redirect("/#badcookie")
    service_user_id, username = user_tuple
    list_of_comments = rating_requests.get_ratings(service_user_id, stars=[1, 2], offset=0, amount=50)
    print(list_of_comments)
    return render_template("cabinet.html", content={"comments": list_of_comments, "service_name": username})


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

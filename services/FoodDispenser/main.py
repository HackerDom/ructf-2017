from flask import Flask, request, jsonify, render_template, redirect
#from uwsgidecorators import cron
from json import loads, JSONDecodeError, dumps
from config import config
from api import api_hub
from database.requests import \
    tokenizer, user_requests, rating_requests, service_requests


app = Flask(__name__, static_folder='static', static_url_path='')


@app.after_request
def patch_response(response):
    response.headers['Content-Security-Policy'] = \
        "default-src 'self' 'unsafe-inline';"
    return response


@app.route("/api/v1/<user_type>/<action>", methods=["POST"])
def registration(user_type, action):
    json_object = get_request_json()
    if json_object:
        return jsonify({"response": api_hub.api_handler.handle_action(
            user_type, action, json_object)})
    else:
        return jsonify({"response": {"error": "Received incorrect data!"}})


def check_cookie():
    cookie = request.cookies.get("token")
    if not cookie:
        raise ValueError()
    user_id, username = tokenizer.verify_token(cookie, "food_service")
    return user_id, username


@app.route("/")
def main_page():
    try:
        check_cookie()
        return redirect("/cabinet")
    except ValueError:
        return render_template("login.html")


@app.route("/set_location", methods=["GET"])
def set_servers_location():
    try:
        user_id, username = check_cookie()
        location = request.args.get("location")
    except (ValueError, KeyError):
        return redirect("/")
    try:
        service_requests.add_service_servers_location(user_id, location)
    except ValueError:
        return redirect("/")
    return redirect("/cabinet")


@app.route("/login", methods=["POST"])
def login_page():
    login = request.form["login"]
    password = request.form["password"]
    try:
        user_id, username, is_food = \
            user_requests.check_user_password(login, password)
        if not is_food:
            raise ValueError()
        token = tokenizer.generate_token(user_id, username, "food_service")
        response = app.make_response(redirect("cabinet"))
        response.set_cookie("token", token)
        return response
    except ValueError:
        return redirect("/#badlogin")


@app.route("/cabinet")
def cabinet_page():
    try:
        user_tuple = check_cookie()
    except ValueError:
        return redirect("/#badcookie")
    service_id, username = user_tuple
    list_of_comments = \
        rating_requests.get_ratings(
            service_id,
            stars=[1, 2],
            offset=0,
            amount=50
        )
    service_loc = service_requests.get_service_servers_location(service_id)
    return render_template(
        "cabinet.html",
        content={
            "comments": dumps(list_of_comments),
            "service_name": username,
            "location": service_loc
        })


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


#@cron(-1, -1, -1, -1, -1)
def dynamically_load_config_changes(_):
    config.update_config()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

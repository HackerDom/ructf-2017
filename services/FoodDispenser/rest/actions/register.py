from rest.rest_hub import rest_handler

@rest_handler.register_action("register", "all")
def register_service_user(json_object):
    return "Maybe, u're registered"

from config import config
from copy import deepcopy
from json import dumps


class ApiHub:
    users_registered_actions = {"food_service": {}, "consumer": {}}

    def handle_action(self, user_type, action, json_data):
        if user_type not in ApiHub.users_registered_actions:
            return {
                "error": "Api doesn't have such user types (\"{}\")!"
                .format(user_type)
            }
        current_actions_dict = ApiHub.users_registered_actions[user_type]

        if action not in current_actions_dict:
            return {
                "error": "\"{}\" doesn't have such actions (\"{}\")!"
                .format(user_type, action)
            }
        callable_action, json_schema = current_actions_dict[action]
        if not callable(callable_action) and callable_action:
            return {
                "error": "Application error"
                # You've got non-callable object in actions dict!
            }

        config_object = deepcopy(config)
        config_object.add(json_data)
        config_object.add({"user_type": user_type})
        if not self.correct_json_schema(config_object.raw, json_schema):
            return {
                "error": "Incorrect json schema, expected: {}"
                .format(dumps(
                    {key: str(value) for key, value in json_schema.items()},
                    indent=4
                ))
            }

        try:
            result = {"result": callable_action(config_object.data)}
        except ValueError as e:
            result = {"error": str(e)}
        except Exception as e:
            print("Uncaught exception:\n{}".format(e))
            result = {"error": "Internal server error!"}

        result.update({
            "requested_action": action,
            "requested_user_type": user_type
        })
        return result

    def correct_json_schema(self, data, json_schema):
        for json_key, json_value in json_schema.items():
            if json_key not in data or\
                    not isinstance(data[json_key], json_value):
                return False
        return True

    @staticmethod
    def register_action(action, destination, json_schema=None):
        """
        :param action: action name, which will be used on defining action
        :param json_schema: checks whether request correct
        :param destination: user type, which will have access to that action
         ('food_service' or 'consumer' or 'all')
        :return: source function
        """
        if not json_schema:
            json_schema = {}

        def wrapper(function):
            if not isinstance(action, str):
                print("Incorrect function (\"{}\") name! Skipping it!"
                      .format(action)
                      )
            else:
                if function.__code__.co_argcount != 1:
                    print("Incorrect argument count in (\"{}\"), skipping it!"
                          .format(action)
                          )
                else:
                    actions_dict = ApiHub.users_registered_actions
                    if destination in actions_dict:
                        actions_dict[destination][action] = \
                            (function, json_schema)
                        print("Registered (\"{}\") to (\"{}\")"
                              .format(action, destination))
                    elif destination.lower() == "all":
                        for dest in actions_dict.keys():
                            actions_dict[dest][action] = \
                                (function, json_schema)
                        print("Registered (\"{}\") to all destinations"
                              .format(action)
                              )
                    else:
                        print("Tried to register function (\"{}\") "
                              "with incorrect destination! Skipping it!"
                              .format(action)
                              )
        return wrapper


api_handler = ApiHub()

from config import config


class RestHub:
    users_registered_actions = {"food_service": {}, "consumer": {}}

    def handle_action(self, user_type, action, json_object):
        if user_type not in RestHub.users_registered_actions:
            return {
                "error": "Api doesn't have such user types (\"{}\")!"
                .format(user_type)
            }
        else:
            current_actions_dict = RestHub.users_registered_actions[user_type]
            if action not in current_actions_dict:
                return {
                    "error": "\"{}\" doesn't have such actions (\"{}\")!"
                    .format(user_type, action)
                }
            else:
                callable_action = current_actions_dict[action]
                if not callable(callable_action) and callable_action:
                    return {
                        "error": "So erroneous, so cute, report it please!;3"
                        # You've got non-callable object in actions dict!
                    }
                else:
                    constants = config.get_constants
                    constants.update(json_object)
                    return {
                        "result": callable_action(constants),
                        "requested_action": action,
                        "requested_user_type": user_type
                    }

    @staticmethod
    def register_action(action, destination):
        """
        :param action: action name, which will be used on defining action
        :param destination: user type, which will have access to that action
         ('food_service' or 'consumer' or 'all')
        :return: source function
        """
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
                    actions_dict = RestHub.users_registered_actions
                    if destination in actions_dict:
                        actions_dict[destination][action] = function
                        print("Registered (\"{}\") to (\"{}\")"
                              .format(action, destination))
                    elif destination.lower() == "all":
                        for dest in actions_dict.keys():
                            actions_dict[dest][action] = function
                        print("Registered (\"{}\") to all destinations"
                              .format(action)
                              )
                    else:
                        print("Tried to register function (\"{}\") "
                              "with incorrect destination! Skipping it!"
                              .format(action)
                              )
        return wrapper


rest_handler = RestHub()

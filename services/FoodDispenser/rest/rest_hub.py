

class RestHub:
    users_registered_actions = {"food_service": {}, "consumer": {}}

    def handle_action(self, user_type, action, json_object):
        if user_type in RestHub.users_registered_actions:
            current_actions_dict = RestHub.users_registered_actions[user_type]
            if action in current_actions_dict:
                callable_action = current_actions_dict[action]
                if callable(callable_action) and callable_action:
                    return {
                        "result": callable_action(json_object),
                        "action": action,
                        "user_type": user_type
                    }
                else:
                    return {
                        "error": "So erroneous, so cute, report it please!;3"
                        # You've got non-callable object in actions dict!
                    }
            else:
                return {
                    "error": "\"{}\" doesn't have such actions (\"{}\")!"
                    .format(user_type, action)
                }
        else:
            return {
                "error": "Api doesn't have such user types (\"{}\")!"
                .format(user_type)
            }

    @staticmethod
    def register_action(action, destination):
        """
        :param action: action name, which will be used on defining action
        :param destination: user type, which will have access to that action
        :return: source function
        """
        def wrapper(function):
            if isinstance(action, str):
                if function.__code__.co_argcount == 1:
                    actions_dict = RestHub.users_registered_actions
                    if destination in actions_dict:
                        actions_dict[destination][action] = function
                        print("Registered (\"{}\") to (\"{}\")"
                              .format(action, destination))
                    elif destination == "all":
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
                else:
                    print("Incorrect argument count in (\"{}\"), skipping it!"
                          .format(action)
                          )
            else:
                print("Incorrect function (\"{}\") name! Skipping it!"
                      .format(action)
                      )
        return wrapper


rest_handler = RestHub()

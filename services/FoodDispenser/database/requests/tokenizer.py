import os
from itsdangerous import \
    TimedJSONWebSignatureSerializer, base64_decode, base64_encode,\
    BadTimeSignature
from database.requests.utils import generate_random_hash

if not os.path.isfile("token_generator.key"):
    with open("token_generator.key", mode="w") as token_file:
        token_file.write(generate_random_hash() + generate_random_hash())

with open("token_generator.key") as token_file:
    secret_key = token_file.read()

serializer = TimedJSONWebSignatureSerializer(secret_key, expires_in=300)


def generate_token(user_id, username, user_group):
    return base64_encode(
        serializer.dumps({
            "id": user_id,
            "username": username,
            "user_group": user_group
        })).decode()


def verify_token(token, user_group=None):
    try:
        user_dict = serializer.loads(base64_decode(token).decode())
        if user_group is not None:
            if user_dict["user_group"] != user_group:
                raise BadTimeSignature("Expected another user type!")
        return user_dict["id"], user_dict["username"]
    except BadTimeSignature as e:
        raise ValueError(str(e))

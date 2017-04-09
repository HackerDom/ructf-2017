from itsdangerous import \
    TimedJSONWebSignatureSerializer, base64_decode, base64_encode,\
    BadTimeSignature


serializer = TimedJSONWebSignatureSerializer("secret-key", expires_in=300)


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
            if user_dict["user_group"] == user_group:
                raise BadTimeSignature("Expected another user type!")
        return user_dict["id"], user_dict["username"]
    except BadTimeSignature as e:
        raise ValueError(str(e))

from itsdangerous import \
    TimedJSONWebSignatureSerializer, base64_decode, base64_encode,\
    BadTimeSignature


serializer = TimedJSONWebSignatureSerializer("secret-key", expires_in=300)


def generate_token(user_id):
    return base64_encode(serializer.dumps({"id": user_id})).decode()


def verify_token(token):
    try:
        return serializer.loads(base64_decode(token).decode())["id"]
    except BadTimeSignature as e:
        raise ValueError(str(e))

import peewee
from datetime import datetime
from peewee import *
from itsdangerous import TimedJSONWebSignatureSerializer as \
    Serializer, BadSignature, SignatureExpired


def init_models(db):
    class AbstractTable(peewee.Model):
        class Meta:
            database = db

    class User(AbstractTable):
        username = CharField(unique=True, max_length=32)
        registration_date = DateTimeField(default=datetime.now)
        password = CharField(max_length=128)
        # fill it

        @staticmethod
        def generate_auth_token(data, expiration=300):
            serializer = Serializer("secret", expires_in=expiration)
            return serializer.dumps({"data": User.username})

        @staticmethod
        def verify_auth_token(token):
            serializer = Serializer("secret")
            try:
                data = serializer.loads(token)
            except SignatureExpired:
                return "Invalid token"
            except BadSignature:
                return "Invalid token"
            return data["data"]
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app.config import Config

token_generator = Serializer(Config.SECRET_KEY, expires_in=Config.TOKEN_LIFETIME)
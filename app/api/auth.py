# API authentication
from flask import g
from flask_httpauth import HTTPBasicAuth
from app.models import User
from app.api.errors import error_response
# for API protecting
from flask_httpauth import HTTPTokenAuth

basic_auth = HTTPBasicAuth()

# API protecting by token
token_auth = HTTPTokenAuth()


# verify password
@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


# error handling
@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


# token verification
@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)

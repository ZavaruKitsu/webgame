import functools

from flask_jwt_extended import JWTManager, current_user, verify_jwt_in_request
from flask_socketio import disconnect

from src.server.Database import DBSession, User

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']

    session = DBSession()

    return session.query(User).filter(User.id == identity).one_or_none()


def ws_authenticated(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        verify_jwt_in_request()

        if not current_user:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped

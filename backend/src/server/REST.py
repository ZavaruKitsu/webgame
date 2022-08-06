from hashlib import sha1

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, current_user, jwt_required

from src.server.Database import DBSession, User

rest = Blueprint('rest', __name__, url_prefix='/rest')

current_user: User


@rest.post('/register')
def register():
    name = request.json['name']
    password = request.json['password']
    avatar = request.json['avatar']

    if not name or not password:
        return jsonify(success=False), 400

    session = DBSession()

    if session.query(session.query(User).filter(User.name == name).exists()).scalar():
        return jsonify(success=False), 400

    user = User()
    user.name = name
    user.password = sha1(password.encode()).hexdigest()
    user.avatar = avatar

    session.add(user)
    session.commit()

    return jsonify(success=True)


@rest.post('/login')
def login():
    name = request.json['name']
    password = request.json['password']

    if not name or not password:
        return jsonify(success=False), 400

    session = DBSession()

    password_hash = sha1(password.encode()).hexdigest()
    user = session.query(User).filter((User.name == name) & (User.password == password_hash)).one_or_none()

    if not user:
        return jsonify(success=False), 400

    token = create_access_token(identity=user)
    return jsonify(success=True, token=token)


@rest.get('/me')
@jwt_required()
def me():
    return jsonify(user={'id': current_user.id, 'name': current_user.name, 'avatar': current_user.avatar})


@rest.get('/scoreboard')
def scoreboard():
    session = DBSession()

    users = session.query(User).all()

    def sorter(x: User):
        s = x.wins + x.looses
        if s == 0:
            return 0

        return x.wins / s

    sort = list(sorted(users, key=sorter, reverse=True))

    return jsonify([player.dictify() for player in sort])

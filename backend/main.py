from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'level': 'debug',
        'format': ' {name:12} {asctime}   {levelname:10} | {message}',
        'datefmt': '%I:%M:%S %p',
        'style': '{'
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    'session': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

from src import KBNamespace, rest, jwt  # noqa

app = Flask(__name__)
app.config['SECRET_KEY'] = '@leXe_yZav@R!!_!!-+!.!Ap!*'
app.config['JWT_SECRET_KEY'] = '@leXe$yZav1@R!!_!!-+!.!Ap!*2'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 9600000
app.config['JWT_TOKEN_LOCATION'] = ['query_string', 'headers']
app.config['COLLECT_MOVES'] = False

CORS(app)
jwt.init_app(app)

app.register_blueprint(rest)

socketio = SocketIO(app, cors_allowed_origins='*')

socketio.on_namespace(KBNamespace(app))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3001)

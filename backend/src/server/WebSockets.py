import datetime
import json
from copy import deepcopy
from typing import Dict

from flask import Flask, request
from flask_jwt_extended import current_user, get_current_user
from flask_socketio import Namespace, join_room

from src.game.AI import AI
from src.server.Authentication import ws_authenticated
from src.server.Database import DBSession, User
from src.server.sessions.LobbyHub import LobbyHub
from src.server.sessions.SessionHub import SessionHub

lobby_hub = LobbyHub()
session_hub = SessionHub()
moves = []


def now():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


class KBNamespace(Namespace):
    def __init__(self, app: Flask):
        super().__init__('/')
        self.app = app

    @ws_authenticated
    def on_disconnect(self):
        if lobby_hub.has_lobby(current_user):
            lobby = lobby_hub.remove_user(current_user)

            if lobby.users:
                self.emit('lobby_updated', lobby.dictify(), room=lobby.lobby_id)
            else:
                lobby_hub.remove_lobby(lobby)

        if session_hub.has_session(current_user):
            session = session_hub.get_session(current_user)
            session.remove_player(current_user)

            if not session.ended:
                db_session = DBSession()
                user = db_session.get(User, current_user.id)
                user.looses += 1

                db_session.commit()

            if session.players and not session.only_bots_alive:
                self.emit('game_updated', session.dictify(), room=session.session_id)
            else:
                session_hub.remove_session(session)

    @ws_authenticated
    def on_create_lobby(self, message=None):
        self.app.logger.warn(f'User {current_user.name} creates lobby.')

        if lobby_hub.has_lobby(current_user):
            self.app.logger.warn('User tried to create a lobby while being in the lobby.')
            return

        lobby, lobby_user = lobby_hub.create_lobby(get_current_user(), message['months'], message['bots'])

        join_room(lobby.lobby_id)

        self.emit('lobby_created', {'lobby_id': lobby.lobby_id}, room=lobby.lobby_id)
        self.emit('lobby_updated', lobby.dictify(), room=lobby.lobby_id)

    @ws_authenticated
    def on_join_lobby(self, message=None):
        lobby_id = message['lobby_id']

        if lobby_hub.has_lobby(current_user):
            self.app.logger.warn('User tried to join a lobby while being in the lobby.')
            self.emit('lobby_probe', {'success': False}, room=request.sid)
            return

        if not lobby_hub.lobby_exists(lobby_id):
            self.app.logger.warn('User tried to join a nonexistent lobby.')
            self.emit('lobby_probe', {'success': False}, room=request.sid)
            return

        join_room(lobby_id)

        lobby, lobby_user = lobby_hub.add_user(lobby_id, get_current_user())

        self.emit('lobby_probe', {'success': True}, room=request.sid)
        self.emit('lobby_updated', lobby.dictify(), room=lobby_id)

    @ws_authenticated
    def on_lobby_user_ready_switch(self, message=None):
        lobby = lobby_hub.get_lobby_by_user(current_user)
        lobby.user_ready_switch(current_user)

        self.emit('lobby_updated', lobby.dictify(), room=lobby.lobby_id)

        if lobby.all_ready:
            session = lobby.create_session()
            session_hub.start_session(session)

            self.emit('game_updated', session.dictify(), room=lobby.lobby_id)
            self.emit('game_started', room=lobby.lobby_id)

            lobby_hub.remove_lobby(lobby)

    @ws_authenticated
    def on_game_send_message(self, message=None):
        session = session_hub.get_session(current_user)

        self.emit('game_new_message', {'user_id': current_user.id, 'date': now(), 'text': message['text']},
                  room=session.session_id)

    @ws_authenticated
    def on_game_make_move(self, message=None):
        session = session_hub.get_session(current_user)

        if self.app.config['COLLECT_MOVES']:
            message_copy: Dict = deepcopy(message)
            message_copy['user'] = session.get_player(current_user).dictify()
            message_copy['market_state'] = session.market_state.dictify(session.p)

            moves.append(message_copy)
            with open('./moves.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(moves))

        session.trigger_move(get_current_user(), **message)

        for message in session.messages_queue:
            self.emit('game_new_message', {'user_id': None, 'date': now(), 'text': message})

        session.messages_queue.clear()

        if session.ended:
            db_session = DBSession()

            alive = session.get_alive_players()

            for player in session.players:
                if isinstance(player, AI):
                    continue

                user = db_session.get(User, player.user.id)
                if player in alive:
                    user.wins += 1
                else:
                    user.looses += 1

            db_session.commit()

            session_hub.remove_session(session)

        self.emit('game_updated', session.dictify(), room=session.session_id)

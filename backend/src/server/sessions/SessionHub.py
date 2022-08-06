import logging
from typing import Dict

from src.game.Session import Session
from src.server.Database import User

logger = logging.getLogger('session_hub')
logger.setLevel(logging.DEBUG)


class SessionHub:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.users: Dict[str, Session] = {}

    def start_session(self, session: Session):
        self.sessions[session.session_id] = session

        for player in session.players:
            self.users[player.user.id] = session

    def get_session(self, user: User):
        return self.users[user.id]

    def has_session(self, user: User):
        return user.id in self.users

    def remove_session(self, session: Session):
        del self.sessions[session.session_id]

        to_remove = []
        for k, v in self.users.items():
            if v.session_id == session.session_id:
                to_remove.append(k)

        for item in to_remove:
            del self.users[item]

        logger.info(f'Removed {session.session_id}')

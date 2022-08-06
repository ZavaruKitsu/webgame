from src.server.Database import User


class LobbyUser:
    def __init__(self, user: User):
        self.user = user
        self.ready = False

    def dictify(self):
        return {
            'user': self.user.dictify(),
            'ready': self.ready
        }

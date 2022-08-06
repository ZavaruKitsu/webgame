from dataclasses import dataclass

from src.server.Database import User


@dataclass(frozen=True)
class AirshipRequest:
    user: User
    amount: int

from dataclasses import dataclass

from src.server.Database import User


@dataclass(frozen=True)
class OreRequest:
    user: User
    amount: int
    price: int

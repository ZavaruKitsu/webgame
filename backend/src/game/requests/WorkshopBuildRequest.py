from dataclasses import dataclass

from src.server.Database import User


@dataclass()
class WorkshopBuildRequest:
    user: User

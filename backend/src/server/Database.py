import uuid

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column('id', Text(length=36), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column('name', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    avatar = Column('avatar', String, nullable=False)
    wins = Column('wins', Integer, nullable=False, default=0)
    looses = Column('looses', Integer, nullable=False, default=0)

    def dictify(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'wins': self.wins,
            'looses': self.looses
        }

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'


engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})  # connect to db
Base.metadata.create_all(engine)  # run init

DBSession = sessionmaker(autoflush=False, bind=engine)

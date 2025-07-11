from datetime import datetime as dt
from typing import List  # Додайте цей імпорт
from models.base import Model

from core import db
from models.relations import association
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Movie(Model, db.Model):
    __tablename__ = 'movies'

    # id -> integer, primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    # name -> string, size 50, unique, not nullable
    name: Mapped[str] = mapped_column(String(50), unique=True)
    # year -> integer
    year: Mapped[int] = mapped_column()
    # genre -> string, size 20
    genre: Mapped[str] = mapped_column(String(20))

    # Use `db.relationship` method to define the Movie's relationship with Actor.
    # Set `backref` as 'filmography', uselist=True
    # Set `secondary` as 'association'
    actors: Mapped[List["Actor"]] = db.relationship('Actor', backref='filmography', uselist=True, secondary=association)

    def __repr__(self):
        return '<Movie {}>'.format(self.name)


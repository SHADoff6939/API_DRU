from datetime import datetime as dt
from typing import List  # Додайте цей імпорт
import sqlalchemy
from models.base import Model

from core import db
from sqlalchemy import String, Date
from models.relations import association
from sqlalchemy.orm import Mapped, mapped_column

class Actor(Model, db.Model):
    __tablename__ = 'actors'

    # id -> integer, primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    # name -> string, size 50, unique, not nullable
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # gender -> string, size 11
    gender: Mapped[str] = mapped_column(String(11), nullable=False)
    # date_of_birth -> date
    date_of_birth: Mapped[dt.date] = mapped_column(Date, nullable=False)

    # Use `db.relationship` method to define the Actor's relationship with Movie.
    # Set `backref` as 'cast', uselist=True
    # Set `secondary` as 'association'
    movies: Mapped[List["Movie"]] = db.relationship('Movie', backref='cast', uselist=True, secondary=association)

    def __repr__(self):
        return '<Actor {}>'.format(self.name)


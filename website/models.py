from . import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Integer, String

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    date_created: Mapped[str] = mapped_column(db.DateTime(timezone= True), default= func.now())

class PopularMovies(db.Model):
    __tablename__ = 'popularmovies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique= True, nullable= False)
    overview: Mapped[str] = mapped_column(String(100), nullable= False)
    poster: Mapped[str] = mapped_column(String(300), nullable= False)
    popularity: Mapped[int] = mapped_column(Integer, nullable= False)
    ranking: Mapped[int] = mapped_column(Integer, nullable= True)
    relase_date: Mapped[str] = mapped_column(String(10), nullable= False)




from . import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    date_created: Mapped[str] = mapped_column(db.DateTime(timezone= True), default= func.now())

    random_movie_rel: Mapped[list["RandomMovie"]] = relationship("RandomMovie", back_populates="user_rel")
    saved_movie_rel : Mapped[list["SaveMovie"]] = relationship("SaveMovie", back_populates="user_rel")

class RandomMovie(db.Model):
    __tablename__ = 'random_movies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    overview: Mapped[str] = mapped_column(String(300), nullable=False)
    relase_date: Mapped[str] = mapped_column(String(10), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable= False)
    poster_url: Mapped[str] = mapped_column(String(300), nullable=False)
    movie_owner: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    user_rel: Mapped[list["User"]] = relationship("User", back_populates="random_movie_rel")

class SaveMovie(db.Model):
    __tablename__ = 'savedmovies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable= False)
    overview: Mapped[str] = mapped_column(String(300), nullable=False)
    relase_date: Mapped[str] = mapped_column(String(10), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable= False)
    poster_url: Mapped[str] = mapped_column(String(300), nullable=False)
    user_who_saved_movie: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    user_rel: Mapped["User"] = relationship("User", back_populates="saved_movie_rel")


class PopularMovies(db.Model):
    __tablename__ = 'popularmovies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique= True, nullable= False)
    overview: Mapped[str] = mapped_column(String(100), nullable= False)
    poster: Mapped[str] = mapped_column(String(300), nullable= False)
    popularity: Mapped[int] = mapped_column(Integer, nullable= False)
    ranking: Mapped[int] = mapped_column(Integer, nullable= True)
    relase_date: Mapped[str] = mapped_column(String(10), nullable= False)

class PopularSeries(db.Model):
    __tablename__ = 'popularseries'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique= True, nullable= False)
    overview: Mapped[str] = mapped_column(String(100), nullable= False)
    poster: Mapped[str] = mapped_column(String(300), nullable= False)
    popularity: Mapped[int] = mapped_column(Integer, nullable= False)
    ranking: Mapped[int] = mapped_column(Integer, nullable= True)
    relase_date: Mapped[str] = mapped_column(String(10), nullable= False)





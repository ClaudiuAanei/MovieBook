from . import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey, Float, Boolean


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable= False)
    password: Mapped[str] = mapped_column(String(100), nullable= False)
    name: Mapped[str] = mapped_column(String(1000), nullable= False)
    confirmation_code: Mapped[str] = mapped_column(String, nullable= False)
    confirmation: Mapped[bool] = mapped_column(Boolean, nullable= False)
    date_created: Mapped[str] = mapped_column(db.DateTime(timezone= True), default= func.now())

    random_movie_rel: Mapped[list["RandomMovie"]] = relationship("RandomMovie", back_populates="user_rel")
    saved_movie_rel : Mapped[list["SaveMovie"]] = relationship("SaveMovie", back_populates="user_rel")

class RandomMovie(db.Model):
    __tablename__ = 'random_movies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    overview: Mapped[str] = mapped_column(String(100), nullable=False)
    poster_url: Mapped[str] = mapped_column(String(300), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    trailer: Mapped[str] = mapped_column(String, nullable=True)
    release_date: Mapped[str] = mapped_column(String(10), nullable=False)

    movie_owner: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    user_rel: Mapped[list["User"]] = relationship("User", back_populates="random_movie_rel")

class SaveMovie(db.Model):
    __tablename__ = 'savedmovies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    overview: Mapped[str] = mapped_column(String(100), nullable=False)
    release_date: Mapped[str] = mapped_column(String(10), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    poster_url: Mapped[str] = mapped_column(String(300), nullable=False)
    trailer: Mapped[str] = mapped_column(String, nullable=True)


    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    user_who_saved_movie: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    user_rel: Mapped["User"] = relationship("User", back_populates="saved_movie_rel")


class PopularMovies(db.Model):
    __tablename__ = 'popularmovies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    overview: Mapped[str] = mapped_column(String(100), nullable=False)
    poster_url: Mapped[str] = mapped_column(String(300), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    trailer: Mapped[str] = mapped_column(String, nullable=True)

    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    release_date: Mapped[str] = mapped_column(String(10), nullable=False)

class PopularSeries(db.Model):
    __tablename__ = 'popularseries'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_id: Mapped[int] = mapped_column(Integer, nullable= False)
    title: Mapped[str] = mapped_column(String(100), unique= True, nullable= False)
    overview: Mapped[str] = mapped_column(String(100), nullable= False)
    poster_url: Mapped[str] = mapped_column(String(300), nullable= False)
    rating: Mapped[float] = mapped_column(Float, nullable= False)
    trailer: Mapped[str] = mapped_column(String, nullable= True)

    ranking: Mapped[int] = mapped_column(Integer, nullable= True)
    release_date: Mapped[str] = mapped_column(String(10), nullable= False)

class Actors(db.Model):
    __tablename__ = 'actors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_name: Mapped[str] = mapped_column(String, nullable=False)
    movie_id: Mapped[int] = mapped_column(Integer, nullable= False)
    character: Mapped[str] = mapped_column(String, nullable= True)
    profile_picture: Mapped[str] = mapped_column(String, nullable= False)
    popularity: Mapped[float] = mapped_column(Float, nullable= True)



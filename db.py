from operator import ge
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker



dbase = declarative_base()


class Users(dbase):
    __tablename__ = "users"
    
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), nullable=False, unique=False)
    token = Column(String(), nullable=False, unique=False)

    mangas = relationship('Mangas')
    
    
    def __init__(self, name, number, number_code):
        self.name = name
        self.number = number
        self.number_code = number_code


class Mangas(dbase):
    __tablename__ = "mangas"
    
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(), nullable=False, unique=False)
    years = Column(String(), nullable=True, unique=False)
    state = Column(String(), nullable=True, unique=False)
    
    users_id = Column(Integer(), ForeignKey("users.id"))
    
    mangas_genres = relationship('Mangas_genres')
    
    
    def __init__(self, title, years, state, users_id):
        self.title = title
        self.years = years
        self.state = state
        self.users_id = users_id
    

class Mangas_genres(dbase):
    __tablename__ = "mangas_genres"
    
    id = Column(Integer(), primary_key=True, autoincrement=True)
    
    mangas_id = Column(Integer(), ForeignKey("mangas.id"))
    genres_id = Column(Integer(), ForeignKey("genres.id"))
    
    
    def __init__(self, mangas_id, genres_id):
        self.mangas_id = mangas_id
        self.genres_id = genres_id
    


class Genres(dbase):
    __tablename__ = "genres"
    
    id = Column(Integer(), primary_key=True, autoincrement=True)
    genre = Column(Integer(), nullable=False, unique=True)
    
    manga_genres = relationship("Mangas_genres")
    
    
    def __init__(self, genre):
        self.genre = genre


def iniciar_db():
    engine = create_engine("sqlite:///regis.db")
    Session = sessionmaker(engine)
    session = Session()
    dbase.metadata.create_all(engine)
    
    return engine, dbase, session

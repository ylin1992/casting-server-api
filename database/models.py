from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, create_engine, Integer, DateTime, ForeignKey, Table
from config import SQLALCHEMY_DATABASE_URI
import datetime

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
# ------------------------------------------------------------
# tables
# ------------------------------------------------------------

gender_actors = Table('gender_actors',
                      db.Model.metadata,
                      Column('gender_id', Integer, ForeignKey('Gender.id')),
                      Column('actor_id', Integer, ForeignKey('Actor.id')),
                      )

actors_movies = Table('actors_movies',
                      db.Model.metadata,
                      Column('actor_id', Integer, ForeignKey('Actor.id')),
                      Column('movie_id', Integer, ForeignKey('Movie.id')),
                      )

class Gender(db.Model):
    # Pre-defined gender
    __tablename__ = 'Gender'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Capable of listing all actor with this gender
    actors = db.relationship('Actor',
                             secondary=gender_actors)
    
    # methods
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

class Movie(db.Model):
    # Movies with attributes title and release date
    
    __tablename__ = 'Movie'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    
    # foreign key
    actors = db.relationship('Actor',
                             secondary=actors_movies,
                             backref=db.backref('movies', lazy=True)
                             )
    
    # methods
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
    
    
class Actor(db.Model):
    # Actors with attributes name, age and gender
    __tablename__ = 'Actor'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # gender: many-to-one relationship
    gender_id = Column(Integer, ForeignKey('Gender.id'))
    
    # foreign key
    movies = db.relationship('Movie',
                             secondary=actors_movies,
                             backref=db.backref('actors', lazy=True)
                             )
    
    # methods
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
    

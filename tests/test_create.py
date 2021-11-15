import os 
import unittest
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask import Flask
import json
from app import create_app
from .unit_test_config import ASSITSTANT_TOKEN, ASSISTANT_AUTH_HEADER, DIRECTOR_AUTH_HEADER, DIRECTOR_TOKEN, PRODCUER_AUTH_HEADER, PRODUCER_TOKEN
from database.models import setup_db, Actor, Movie, Gender
from sqlalchemy import func


class TestCastingApi(unittest.TestCase):
    
    def setUp(self):
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PWD  = os.getenv('DB_PWD', 'postgres')
        DB_NAME = os.getenv('DB_TEST_NAME', 'casting_test')
        database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_NAME)
        self.app = create_app()
        self.client = self.app.test_client

        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            self.drop_data()
            self.populate_data()
            print('metadata from test: ', self.db.metadata.tables)
    def tearDown(self):
        pass     
    
    # def test_sth(self):
    #     self.assertTrue(True)

    # def test_200_delete_actor_with_existing_id(self):
    #     actors_before = Actor.query.all()
    #     res = self.client().delete('/actors/1', headers=PRODCUER_AUTH_HEADER)
    #     actors_after = Actor.query.all()
        
    #     data = json.loads(res.data)
        
    #     exists = False
    #     for actor in actors_after:
    #         if actor.id == 1:
    #             exists = True
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertFalse(exists)
    #     self.assertEqual(len(actors_before) - len(actors_after), 1)
    #     self.assertTrue('delete' in data)
    #     self.assertEqual(data['delete'], 1)
            
    def populate_data(self):
        genders = Gender.query.all()
        if (genders is None) or (len(genders) == 0):
            Gender(id=1, name='m').insert()
            Gender(id=2, name='f').insert()
        
        actors = [
            Actor(name='a1', age=1, gender_id=1),
            Actor(name='a2', age=2, gender_id=2),
            Actor(name='a3', age=1, gender_id=1),
            Actor(name='a4', age=2, gender_id=2),
            Actor(name='a5', age=1, gender_id=1),
            Actor(name='a6', age=2, gender_id=2),
            Actor(name='a7', age=1, gender_id=1),
            Actor(name='a8', age=2, gender_id=2),
        ]
        
        actors[0].id = 1
        actors[0].update()
        
        for i, actor in enumerate(actors):
            # actor.id = i + 1
            actor.insert()
            
        movies = [
            Movie(title='m1', release_date='2019-05-23T21:30:00.000Z'),
            Movie(title='m2', release_date='2018-05-23T21:30:00.000Z'),
            Movie(title='m3', release_date='2019-05-23T21:30:00.000Z'),
            Movie(title='m4', release_date='2017-05-23T21:30:00.000Z'),
            Movie(title='m5', release_date='2019-05-23T21:30:00.000Z'),
            Movie(title='m6', release_date='2012-05-23T21:30:00.000Z'),
            Movie(title='m7', release_date='2013-05-23T21:30:00.000Z'),
            Movie(title='m8', release_date='2011-05-23T21:30:00.000Z')
        ]
        
        movies[0].id = 1
        movies[0].update()
        for i, movie in enumerate(movies):
            # movie.id = i + 1
            movie.insert()
            
        # assign some testing movies for actors[1, 2]
        actors[0].movies = [movies[i] for i in [1,2,3,4,5]]
        actors[2].movies = [movies[i] for i in [1,2,3,4,6]]
        actors[1].update()
        actors[2].update()
        
        movies[0].actors = [actors[i] for i in [2,3,4,5,6]]
        movies[0].update()
        for i in range(3,7):
            actors[i].movies = [movies[7]]
            actors[i].update()
            
    def drop_data(self):
        Movie.query.delete()
        Actor.query.delete()
        self.db.session.execute("ALTER SEQUENCE actor_id_seq RESTART WITH 1")
        self.db.session.execute("ALTER SEQUENCE movie_id_seq RESTART WITH 1")
        self.db.session.commit()

if __name__ == '__main__':
    unittest.main()
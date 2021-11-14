import os 
import unittest
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask import Flask
import json
from app import create_app
from database.models import setup_db, Actor, Movie, Gender
from .unit_test_config import ASSITSTANT_TOKEN, ASSISTANT_AUTH_HEADER, DIRECTOR_AUTH_HEADER, DIRECTOR_TOKEN, PRODCUER_AUTH_HEADER, PRODUCER_TOKEN



class TestCastingApi(unittest.TestCase):

    def setUp(self):
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PWD  = os.getenv('DB_PWD', 'postgres')
        DB_NAME = os.getenv('DB_TEST_NAME', 'casting_test')
        database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_NAME)
        self.app = create_app()
        self.client = self.app.test_client

        self.db = setup_db(self.app, database_path=database_path)
        with self.app.app_context():
            self.db.create_all()
            self.drop_data()
            self.populate_data()
            self.db.session.commit()
        
            
    def tearDown(self):
        pass

    # ------------------------------------------------------------------ 
    # actors: GET
    # ------------------------------------------------------------------ 
    def test_401_get_actors_with_invalid_header(self):
        res1 = self.client().get('/actors', headers={'invalid_header': 'invlalid_token'})
        res2 = self.client().get('/actors/1', headers={'invalid_header': 'invlalid_token'})
        
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(res2.status_code, 401)
        
    def test_401_get_actors_with_invalid_token(self):
        res1 = self.client().get('/actors', headers={'Bearer': 'invlalid_token'})
        res2 = self.client().get('/actors/1', headers={'Bearer': 'invlalid_token'})
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(res2.status_code, 401)
    # ------------------------------------------------------------------ 
    # actors: POST
    # ------------------------------------------------------------------ 
    def test_401_post_actors_with_invalid_header(self):
        res1 = self.client().post('/actors', headers={'invalid_header': 'invlalid_token'}, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 401)
    
    def test_401_post_actors_with_invalid_token(self):
        res1 = self.client().post('/actors', headers={'Bearer': 'invlalid_token'}, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 401)
    
    def test_403_post_actors_with_unauthorized_token(self):
        res1 = self.client().post('/actors', headers=ASSISTANT_AUTH_HEADER, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 403)
    
    def test_200_post_actors_with_authorized_token(self):
        res1 = self.client().post('/actors', headers=DIRECTOR_AUTH_HEADER, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        res2 = self.client().post('/actors', headers=PRODCUER_AUTH_HEADER, json={'name': 'test_name2', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        
    # ------------------------------------------------------------------ 
    # actors: DELETE
    # ------------------------------------------------------------------ 
    def test_401_delete_actors_with_invalid_header(self):
        res1 = self.client().delete('/actors/1', headers={'invalid_header': 'invlalid_token'})
        self.assertEqual(res1.status_code, 401)
    
    def test_401_delete_actors_with_invalid_token(self):
        res1 = self.client().delete('/actors/1', headers={'Bearer': 'invlalid_token'})
        self.assertEqual(res1.status_code, 401)
    
    def test_403_delete_actors_with_unauthorized_token(self):
        res1 = self.client().delete('/actors/1', headers=ASSISTANT_AUTH_HEADER)
        self.assertEqual(res1.status_code, 403)
    
    def test_200_delete_actors_with_authorized_token(self):
        res1 = self.client().delete('/actors/1', headers=DIRECTOR_AUTH_HEADER)
        res2 = self.client().delete('/actors/2', headers=PRODCUER_AUTH_HEADER)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

    # ------------------------------------------------------------------ 
    # actors: PATCH
    # ------------------------------------------------------------------ 
    def test_401_patch_actors_with_invalid_header(self):
        res1 = self.client().patch('/actors/1', headers={'invalid_header': 'invlalid_token'}, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 401)
    
    def test_401_patch_actors_with_invalid_token(self):
        res1 = self.client().patch('/actors/1', headers={'Bearer': 'invlalid_token'}, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 401)
    
    def test_403_patch_actors_with_unauthorized_token(self):
        res1 = self.client().patch('/actors/1', headers=ASSISTANT_AUTH_HEADER, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 403)
    
    def test_200_patch_actors_with_authorized_token(self):
        res1 = self.client().patch('/actors/1', headers=DIRECTOR_AUTH_HEADER, json={'name': 'test_name', 'gender': 'm', 'age': 11})
        res2 = self.client().patch('/actors/2', headers=PRODCUER_AUTH_HEADER, json={'name': 'test_name2', 'gender': 'm', 'age': 11})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
    
    # --------------- movie routes ---------------

    # ------------------------------------------------------------------ 
    # movies: GET
    # ------------------------------------------------------------------ 
    def test_401_get_movies_with_invalid_header(self):
        res1 = self.client().get('/movies', headers={'invalid_header': 'invlalid_token'})
        res2 = self.client().get('/movies/1', headers={'invalid_header': 'invlalid_token'})
        
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(res2.status_code, 401)
        
    def test_401_get_movies_with_invalid_token(self):
        res1 = self.client().get('/movies', headers={'Bearer': 'invlalid_token'})
        res2 = self.client().get('/movies/1', headers={'Bearer': 'invlalid_token'})
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(res2.status_code, 401)    

    # ------------------------------------------------------------------ 
    # movies: POST
    # ------------------------------------------------------------------ 
    def test_401_post_movies_with_invalid_header(self):
        res1 = self.client().post('/movies', headers={'invalid_header': 'invlalid_token'}, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 401)
    
    def test_401_post_movies_with_invalid_token(self):
        res1 = self.client().post('/movies', headers={'Bearer': 'invlalid_token'}, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 401)
    
    def test_403_post_movies_with_unauthorized_token(self):
        res1 = self.client().post('/movies', headers=ASSISTANT_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        res2 = self.client().post('/movies', headers=DIRECTOR_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 403)
        self.assertEqual(res2.status_code, 403)
    
    def test_200_post_movies_with_authorized_token(self):
        res1 = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 200)
        
    # ------------------------------------------------------------------ 
    # movies: DELETE
    # ------------------------------------------------------------------ 
    def test_401_delete_movies_with_invalid_header(self):
        res1 = self.client().delete('/movies/1', headers={'invalid_header': 'invlalid_token'})
        self.assertEqual(res1.status_code, 401)
    
    def test_401_delete_movies_with_invalid_token(self):
        res1 = self.client().delete('/movies/1', headers={'Bearer': 'invlalid_token'})
        self.assertEqual(res1.status_code, 401)
    
    def test_403_delete_movies_with_unauthorized_token(self):
        res1 = self.client().delete('/movies/1', headers=ASSISTANT_AUTH_HEADER)
        res2 = self.client().delete('/movies/1', headers=DIRECTOR_AUTH_HEADER)
        self.assertEqual(res1.status_code, 403)
        self.assertEqual(res2.status_code, 403)

    def test_200_delete_movies_with_authorized_token(self):
        res1 = self.client().delete('/movies/2', headers=PRODCUER_AUTH_HEADER)
        self.assertEqual(res1.status_code, 200)

    # ------------------------------------------------------------------ 
    # movies: PATCH
    # ------------------------------------------------------------------ 
    def test_401_patch_movies_with_invalid_header(self):
        res1 = self.client().patch('/movies/1', headers={'invalid_header': 'invlalid_token'}, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 401)
    
    def test_401_patch_movies_with_invalid_token(self):
        res1 = self.client().patch('/movies/1', headers={'Bearer': 'invlalid_token'}, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 401)
    
    def test_403_patch_movies_with_unauthorized_token(self):
        res1 = self.client().patch('/movies/1', headers=ASSISTANT_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 403)
    
    def test_200_patch_movies_with_authorized_token(self):
        res1 = self.client().patch('/movies/1', headers=DIRECTOR_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        res2 = self.client().patch('/movies/2', headers=PRODCUER_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
  
    # ------------------------------------------------------------------ 
    # helper functions
    # ------------------------------------------------------------------ 
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
        for i, actor in enumerate(actors):
            actor.id = i + 1
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
        
        for i, movie in enumerate(movies):
            movie.id = i + 1
            movie.insert()
            
        # assign some testing movies for actors[1, 2]
        actors[1].movies = [movies[i] for i in [1,2,3,4,5]]
        actors[2].movies = [movies[i] for i in [1,2,3,4,6]]
        actors[1].update()
        actors[2].update()
            
    def drop_data(self):
        Movie.query.delete()
        Actor.query.delete()
        self.db.session.commit()

        
if __name__ == '__main__':
    unittest.main()
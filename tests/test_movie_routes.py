import os 
import unittest
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask import Flask
import json
from app import create_app
from database.models import setup_db, Actor, Movie, Gender
from .unit_test_config import ASSITSTANT_TOKEN, ASSISTANT_AUTH_HEADER, DIRECTOR_AUTH_HEADER, DIRECTOR_TOKEN, PRODCUER_AUTH_HEADER, PRODUCER_TOKEN
import datetime

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
    # movies: GET
    # ------------------------------------------------------------------ 
    def test_get_all_movies(self):
        res = self.client().get('/movies', headers=PRODCUER_AUTH_HEADER)
        data = json.loads(res.data)
        expected = Movie.query.all()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue('movies' in data)
        self.assertEqual(len(data['movies']), len(expected))
        self.assertTrue(data['success'])

    def test_empty_movies(self):
        with self.app.app_context():
            self.drop_data()
            self.db.session.commit()
            res = self.client().get('/movies', headers=PRODCUER_AUTH_HEADER)
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertTrue('movies' in data)
            self.assertEqual(len(data['movies']), 0)
            self.assertTrue(data['success'])
            
    def test_200_get_movies_by_existing_id(self):
        res = self.client().get('/movies/1', headers=PRODCUER_AUTH_HEADER)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('movie' in data)
        self.assertEqual(data['movie']['id'], 1)
        
    def test_404_get_movie_with_unknown_id(self):
        res = self.client().get('/movies/1000000000000000', headers=PRODCUER_AUTH_HEADER)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_404_get_movie_with_invalid_query(self):
        res = self.client().get('/actors/ghjhglkshglkjs', headers=PRODCUER_AUTH_HEADER)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_200_get_actors_by_movie_id(self):
        res = self.client().get('/movies/1/actors', headers=PRODCUER_AUTH_HEADER)
        data = json.loads(res.data)
        movie = Movie.query.filter_by(id=1).one_or_none()
        expected_aid = [actor.id for actor in movie.actors]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['actors_id']), len(expected_aid))
        for a_id in data['actors_id']:
            self.assertIn(a_id, expected_aid)
        
    def test_404_get_actors_with_unknown_movie_id(self):
        res = self.client().get('/movies/2000/actors', headers=PRODCUER_AUTH_HEADER)
        self.assertEqual(res.status_code, 404)
        
    # ------------------------------------------------------------------ 
    # movies: DELETE
    # ------------------------------------------------------------------ 
    
    def test_200_delete_actor_with_existing_id(self):
        movies_before = Movie.query.all()
        res = self.client().delete('/movies/1', headers=PRODCUER_AUTH_HEADER)
        movies_after = Movie.query.all()
        
        data = json.loads(res.data)
        
        exists = False
        for movie in movies_after:
            if movie.id == 1:
                exists = True
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(exists)
        self.assertEqual(len(movies_before) - len(movies_after), 1)
        self.assertTrue('delete' in data)
        self.assertEqual(data['delete'], 1)
        
    def test_404_delete_movie_with_invlaid_id(self):
        res = self.client().delete('/movies/100', headers=PRODCUER_AUTH_HEADER)
        data = json.loads(res.data)
        
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)
        
    # ------------------------------------------------------------------ 
    # movies: POST
    # ------------------------------------------------------------------  
    
    def test_200_post_movie_with_sufficient_input(self):
        res = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'title': 'test_name', 'release_date': '2019-05-23T21:30:00.000Z'})
        data = json.loads(res.data)
        
        movie = Movie.query.filter_by(title='test_name').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(movie)
    
        
    def test_400_post_movie_with_insufficient_input(self):
        res1 = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'title': 'test_name'})
        res2 = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'release_date': '2019-05-23T21:30:00.000Z'})
        res3 = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'title': 'test_name', 'release_date': ''})
        res4 = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'title': '', 'release_date': '2019-05-23T21:30:00.000Z'})

        self.assertEqual(res1.status_code, 400)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res3.status_code, 400)
        self.assertEqual(res4.status_code, 400)
        
    def test_422_post_movie_with_sufficient_but_invalid_input(self):
        res1 = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'title': 'test_name', 'release_date': 'fsj'})
        res2 = self.client().post('/movies', headers=PRODCUER_AUTH_HEADER, json={'title': 123, 'release_date': '2019-05-23T21:30:00.000Z'})
        self.assertEqual(res1.status_code, 422)
        self.assertEqual(res2.status_code, 422)

    
        
    # ------------------------------------------------------------------ 
    # movies: PATCH
    # ------------------------------------------------------------------ 
    
    def test_200_pacth_movie_with_normal_input(self):
        res = self.client().patch('/movies/1', headers=PRODCUER_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        data = json.loads(res.data)
        
        movie = Movie.query.filter_by(id=1).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(movie)
        self.assertEqual(movie.title, 'modified')
        self.assertEqual(movie.release_date, datetime.datetime(3030, 5, 23, 21, 30))
        
        
    def test_400_patch_movie_with_invalid_key(self):
        res = self.client().patch('/movies/1', headers=PRODCUER_AUTH_HEADER, json={'unknown_key':'unknown_value'})
        self.assertEqual(res.status_code, 400)

    def test_404_patch_movie_with_unknown_id(self):
        res1 = self.client().patch('/movies/1000', headers=PRODCUER_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        res2 = self.client().patch('/movies/sfsfsd', headers=PRODCUER_AUTH_HEADER, json={'title':'modified', 'release_date': '3030-05-23T21:30:00.000Z'})
        
        self.assertEqual(res1.status_code, 404)
        self.assertEqual(res2.status_code, 404)
    
    def test_404_patch_movies_with_unknown_actor_id(self):
        res = self.client().patch('/movies/1', headers=PRODCUER_AUTH_HEADER, json={'actors': [10000]})
        self.assertEqual(res.status_code, 400)
        
    
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
        
        # actors[0].id = 1
        # actors[0].update()
        
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
        
        # movies[0].id = 1
        # movies[0].update()
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
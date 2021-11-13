import os 
import unittest
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask import Flask
import json
from app import create_app
from database.models import setup_db, Actor, Movie, Gender


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
    def test_get_all_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        expected = Actor.query.all()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue('actors' in data)
        self.assertEqual(len(data['actors']), len(expected))
        self.assertTrue(data['success'])

    def test_empty_actors(self):
        with self.app.app_context():
            self.drop_data()
            self.db.session.commit()
            res = self.client().get('/actors')
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertTrue('actors' in data)
            self.assertEqual(len(data['actors']), 0)
            self.assertTrue(data['success'])
            
    def test_200_get_actors_by_existing_id(self):
        res = self.client().get('/actors/3')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('actor' in data)
        self.assertEqual(data['actor']['id'], 3)
        
    def test_404_get_actor_with_unknown_id(self):
        res = self.client().get('/actors/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_404_get_actor_with_invalid_query(self):
        res = self.client().get('/actors/ghjhglkshglkjs')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_200_get_movies_by_actor_id(self):
        res = self.client().get('/actors/2/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['movies_id']), 5)
        for m_id in data['movies_id']:
            self.assertTrue(m_id in [2,3,4,5,6])
        
    def test_404_get_movies_with_unknown_actor_id(self):
        res = self.client().get('/actors/2000/movies')
        self.assertEqual(res.status_code, 404)
        
    # ------------------------------------------------------------------ 
    # actors: DELETE
    # ------------------------------------------------------------------ 
    
    def test_200_delete_actor_with_existing_id(self):
        actors_before = Actor.query.all()
        res = self.client().delete('/actors/1')
        actors_after = Actor.query.all()
        
        data = json.loads(res.data)
        
        exists = False
        for actor in actors_after:
            if actor.id == 1:
                exists = True
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(exists)
        self.assertEqual(len(actors_before) - len(actors_after), 1)
        self.assertTrue('delete' in data)
        self.assertEqual(data['delete'], 1)
        
    def test_404_delete_actor_with_invlaid_id(self):
        res = self.client().delete('/actors/100')
        data = json.loads(res.data)
        
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)
        
    # ------------------------------------------------------------------ 
    # actors: POST
    # ------------------------------------------------------------------  
    
    def test_200_post_actor_with_sufficient_input(self):
        res = self.client().post('/actors', json={'name': 'test_name', 'gender': 'm', 'age': 11})
        data = json.loads(res.data)
        
        actor = Actor.query.filter_by(name='test_name') \
                           .filter_by(gender_id=1) \
                           .filter_by(age=11).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(actor)
    
    def test_200_post_actor_with_convertable_name(self):
        res = self.client().post('/actors', json={'name': 123, 'gender': 'm', 'age': 11})
        data = json.loads(res.data)
        actor = Actor.query.filter_by(name='123') \
                    .filter_by(gender_id=1) \
                    .filter_by(age=11).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(actor)
        
    def test_400_post_actor_with_insufficient_input(self):
        res1 = self.client().post('/actors', json={'name': 'test_name', 'gender': 'm'})
        res2 = self.client().post('/actors', json={'age': 11, 'gender': 'm'})
        res3 = self.client().post('/actors', json={'name': 'test_name', 'age': 11})
        
        self.assertEqual(res1.status_code, 400)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res3.status_code, 400)

    def test_500_post_actor_with_sufficient_but_invalid_input(self):
        res1 = self.client().post('/actors', json={'name': 'test_name', 'gender': 'm', 'age': 'jfs'})
        self.assertEqual(res1.status_code, 500)
    
    def test_400_post_invalid_gender(self):
        res1 = self.client().post('/actors', json={'name': 'test_name', 'gender': 'X', 'age': 11})
        res2 = self.client().post('/actors', json={'name': 'test_name', 'gender': 1, 'age': 11})
        res3 = self.client().post('/actors', json={'name': 'test_name', 'gender': '', 'age': 11})
        
        self.assertEqual(res1.status_code, 400)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res3.status_code, 400)
        
    # ------------------------------------------------------------------ 
    # actors: PATCH
    # ------------------------------------------------------------------ 
    
    def test_200_pacth_actor_with_normal_input(self):
        res = self.client().patch('/actors/1', json={'name':'modified', 'age':10, 'gender': 'f', 'movies': [2,3,4]})
        data = json.loads(res.data)
        
        actor = Actor.query.filter_by(id=1).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(actor)
        self.assertEqual(actor.name, 'modified')
        self.assertEqual(actor.gender_id, 2)
        self.assertEqual(actor.age, 10)
        self.assertEqual(actor.name, data['actor']['name'])
        self.assertEqual('f', data['actor']['gender'])
        self.assertEqual(actor.age, data['actor']['age'])
        for movie_id in data['actor']['movies']:
            self.assertTrue(movie_id in [2,3,4])
        
        # test appending data
        res2 = self.client().patch('/actors/1', json={'movies': [1,2,3,4]})
        data = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['actor']['movies']), 4)
        for movie_id in data['actor']['movies']:
            self.assertTrue(movie_id in [1,2,3,4])
        
        
    def test_400_patch_actor_with_invalid_key(self):
        res = self.client().patch('/actors/1', json={'unknown_key':'unknown_value'})
        self.assertEqual(res.status_code, 400)

    def test_404_patch_actor_with_unknown_id(self):
        res1 = self.client().patch('/actors/1000', json={'name':'modified', 'age':10, 'gender': 'f'})
        res2 = self.client().patch('/actors/sfsfsd', json={'name':'modified', 'age':10, 'gender': 'f'})
        
        self.assertEqual(res1.status_code, 404)
        self.assertEqual(res2.status_code, 404)
    
    def test_400_patch_actor_with_invalid_gender(self):
        res1 = self.client().patch('/actors/1', json={'name': 'test_name', 'gender': 'X', 'age': 11})
        res2 = self.client().patch('/actors/1', json={'name': 'test_name', 'gender': 1, 'age': 11})
        res3 = self.client().patch('/actors/1', json={'name': 'test_name', 'gender': '', 'age': 11})
        
        self.assertEqual(res1.status_code, 400)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res3.status_code, 400)
    
    def test_404_patch_actor_with_unknown_movie_id(self):
        res = self.client().patch('/actors/1', json={'movies': [10000]})
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
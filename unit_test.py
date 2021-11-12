import os 
import unittest

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import json
from app import create_app
from database.models import setup_db, Actor, Movie, Gender

class TestCastingApi(unittest.TestCase):
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PWD  = os.getenv('DB_PWD', 'postgres')
    DB_NAME = os.getenv('DB_TEST_NAME', 'casting_test')
    database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_NAME)

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, database_path=self.database_path)
        self.engine = sqlalchemy.create_engine(self.database_path)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()
            self.db.session.commit()
            # self.drop_data()
            # self.populate_data()
    
    def test_get_all_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        expected = Actor.query.all()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']), len(expected))
        self.assertTrue(data['success'])

    
    def populate_data(self):
        genders = Gender.query.all()
        if (genders is None) or (len(genders) == 0):
            Gender(id=1, name='m').insert()
            Gender(id=2, name='f').insert()
        
        actors = [
            Actor(name='a1', age=1, gender_id=1),
            Actor(name='a2', age=2, gender_id=2),
        ]
        for actor in actors:
            actor.insert()
            
        movies = [
            Movie(title='m1', release_date='2019-05-23T21:30:00.000Z'),
            Movie(title='m1', release_date='2020-05-23T21:30:00.000Z')
        ]
        
        for movie in movies:
            movie.insert()
            
    def drop_data(self):
        Movie.query.delete()
        Actor.query.delete()
        
if __name__ == '__main__':
    unittest.main()
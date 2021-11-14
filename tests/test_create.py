import os 
import unittest
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask import Flask
import json
from app import create_app
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

        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        with self.app.app_context():
            self.db = SQLAlchemy(self.app)
            from database import models
            print('metadata from test: ', self.db.metadata.tables)
            self.db.create_all()
            self.db.session.commit()
    def tearDown(self):
        pass     
    
    def test_sth(self):
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

Casting_Assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYWUxMTM2OGJjNjBjMGFmMzg4ZWUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYwMTM5MCwiZXhwIjoxNTkxNjA4NTkwLCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.dF0ABVznnmBIM_Jkn6RVUqeKXU8auMIKJ9DYDezVJ5GH27tEZbKGOBY-PYm6Ns9vg590VRnIRyf5CAw384ZxEjarU8uUjLPBsb5AsMY-QPHdHSh2EocZ0aOmCgNYnUbfmJpivgjnNACw5EHutpCbihIiSd6hbYXI79VIOK0Q4hj5rF2mH1GNfBWTzhmA6nUtDeJ0-UJdn3zXdx1QB_L55vPJPe3nDyhxYYqDPlu_XysITy9l42ihHHh54xK2gB2ufteX-SQWtVNem_Q7LRZffkvmRLdXR8T3iMAxHRzqdmgWgS6HumtuCrmaebsetG8vDMM9i6SjC2Z56xLmIQnATw'
Casting_Director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYWUxMTM2OGJjNjBjMGFmMzg4ZWUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYwMTYwMSwiZXhwIjoxNTkxNjA4ODAxLCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.NSQeccEUrPkJbt4yubooeSKJhKoDQVkwN5ZNFOW44WJuHFkNhkOmvl_bwEi4OD0iu8fGQ-hNg_KTLGlIJmG0oFxg0ekgnXwPSXUHof4IPHjbbyBhVr91AKGrwDMepf2t-vUT1p3qm0LIFlEWLku4mkqXLxZBvpCKU1-QwFriS9YSd9VSx5WLSv8Pm5e4T8Wkl30qSn_iIqtrCZd0qzx5qMWmHMi4cC5w_TWAXMxeRS9wZWRLIV4tuNai0j2qbVQjKWU54spXxyPC7MwYS1CaTst2i-yJwH77UzvJ7Fs6OTMiY4KbQZFmDh5CG8MgjaAJB0hpNyNpzyxfbwZQhuffmg'
Executive_Producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYjAyOTcyODA0MTBjMWJiNWZlYWEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYwMTY2NSwiZXhwIjoxNTkxNjA4ODY1LCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.Fyp2uWsODKJlLr0yuAs_G9FoYJ0cImIRjp0HTZ2NUP6jd_-MGelPgjNGWwjA7eMLI0lcEFxZOa7vNRA-bsdWJSU94vKyeCVxKlqYZ0vz7s-EExCXGeulszUoGLiacuUK8gQODmrFZjHE_ZfuH2mnkyzS3hWXrEzqRWjTU42SqW9BCdZPyQEsuB_ljNecsHX1DyswTX6i76B8tccNwOUGt8KQLuFmFD6Tgnpqaqc-2ncUOaqHvxaD7k-AOoZofHzNJMGfjSjJwKdto_ICPIK8BZXJqIZixJVRkaM5cG7xltR2fQ8QW73x_90vpZPKzVess8bu36J_iPnUN1NzEpgH3g'


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        # self.database_path = os.environ["TEST_DATABASE_URL"]
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'Noa',
            'age': 27,
            'gender': 'both'
        }

        self.new_movie = {
            'title': 'GreatMovie',
            'release_date': '1999'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers={"Authorization": "Bearer" + Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers={"Authorization": "Bearer" + Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/1', headers={"Authorization": "Bearer" + Casting_Director})
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    def test_delete_nonexisting_actor(self):
        res = self.client().delete(
            '/actors/10000', headers={"Authorization": "Bearer" + Casting_Director})
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 10000).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1', headers={"Authorization": "Bearer" + Executive_Producer})
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_delete_movie_with_wrong_permission(self):
        res = self.client().delete(
            '/movies/2', headers={"Authorization": "Bearer" + Casting_Assistant})
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 2).one_or_none()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": "Bearer" + Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['created'])
        self.assertEqual(len(data['actors']))

    def test_create_new_actor_wrong_permission(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": "Bearer" + Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_create_new_movie(self):
        res = self.client().post('/moview', json=self.new_movie,
                                 headers={"Authorization": "Bearer" + Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['created'])
        self.assertEqual(len(data['movies']))

    def test_create_new_movie_wrong_permission(self):
        res = self.client().post('/moview', json=self.new_movie,
                                 headers={"Authorization": "Bearer" + Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_update_actor(self):
        res = self.client().patch('/actors/3', json={'age': 50})
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.fomrat()['age'], 50)

    def test_failed_update_actor(self):
        res = self.client().patch('/actors/300', json={'age': 50})
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 300).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


if __name__ == "__main__":
    unittest.main()

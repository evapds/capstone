import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

Casting_Assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYWUxMTM2OGJjNjBjMGFmMzg4ZWUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYxMDA2NCwiZXhwIjoxNTkxNjk2NDY0LCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.NWUmhRPt4ji-lFAX4gUWc4OLjucM1VRtX-I07vNg8m8vIyJcA7Iq5UG6sdQzKznrX1kd60-Ux5ABkExxXhqkuy4-OVACAXF9cMQFTgRpK4oCJ8E6kSru8kjHaqwptmDaej_Tu0dYfLZgxEIo_Gw7Z3K5oAq7F85uiDkqBANWKVHqAF6yfgXYtvxxFkt1Mtvli2fZ16O_WD5TDjukgNL1Pep3X1WZGd2N6R230EbXD8Z_DHz_NZllhzyw7E2Y2Fl8zTCaovSljFsQj5CdKZL0cYfe6v7vuXXzJx9dCDwE_89keLqUT7I5Q7KuWyGg48unKyBXbR2KuP90F2GjrcDGQw'
Casting_Director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYWUxMTM2OGJjNjBjMGFmMzg4ZWUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYwOTg4NCwiZXhwIjoxNTkxNjE3MDg0LCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.Ca2xuCcCWLrVF_cnUofVtKsN-XGiGzKCkjtJVwgFdwmnB0bBLr9qcYK9sYBeb5DcEP-Ff7ZPr9FG-CsNuMapOSX_378dPqrUQ9qUzPUp22i8lQuvCvYSS9ikesYout1PQez1p8ACCCyEQnprc2wNO1ARB7Db1chahJWhLx93KCbAfg8-Wi4ZTVfJSbkuJ8_8w-o66eHcatlgpNCtQYTrd2cUxhIVQhwxLphaqDSPMNM9VLaN6tjjBxDz5yjQXTSL2_dVoltks_IRQYQG2BfbzGw5K6plTSgdMJuvA1-rDOdqQYmG3_166BWmlxCjHQmzMdM8fbNlO4mX42DgdlRKoQ'
Executive_Producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYjAyOTcyODA0MTBjMWJiNWZlYWEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYwOTkyOCwiZXhwIjoxNTkxNjE3MTI4LCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.scipRwUMn94yJv91j0KnSeKlvpZUPnYPSkJMaV0OzlIRZpxkbcoZrrHEm3qbRdUph307wfRDNtA5dxBLH2AAgS0gj4DzoZpAHZTtrjEDd-qizTfX0ZYHBFbvzl-tXgZnqLb_jv3pt0dzmuH71ra_fZu07FATaFRRDcMdTKQLpno4sMQiTNr2iTHOHmDrYBkwdrQNy9elbDAq4fvuUa8tnLeEolPt1_KDrNXRAY09F8twDjCk99jBuQC1ON2MFz8XuBcVjs7alKOx-Y310NGPS-XRDTJNvF2a7i2srxxkJVsERbEpi_tXcTsnSnkS-4v4C1QdfN6NDmUe_7CXTa3NTA'


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
            'name': 'Ariane',
            'age': 48,
            'gender': 'female'
        }

        self.new_movie = {
            'title': 'Sad movie',
            'release_date': '1987'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers={"Authorization": "Bearer " + Casting_Assistant})
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers={"Authorization": "Bearer " + Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/3', headers={"Authorization": "Bearer " + Casting_Director})
        print(res)
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    def test_delete_nonexisting_actor(self):
        res = self.client().delete(
            '/actors/10000', headers={"Authorization": "Bearer " + Casting_Director})
        print(res)
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 10000).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/4', headers={"Authorization": "Bearer " + Executive_Producer})
        print('delete movie', res)
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    def test_delete_movie_with_wrong_permission(self):
        res = self.client().delete(
            '/movies/6', headers={"Authorization": "Bearer " + Casting_Assistant})
        print('movie deletion wrong permission', res)
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 6).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": "Bearer " + Executive_Producer})
        print('new actor', res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_new_actor_wrong_permission(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": "Bearer " + Casting_Assistant})
        print('new actor wrong permission', res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": "Bearer " + Executive_Producer})
        print('new movie', res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_new_movie_wrong_permission(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": "Bearer " + Casting_Assistant})
        print('new movie wrong permission', res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    def test_update_actor(self):
        res = self.client().patch('/actors/19', json={'age': 13},
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        print('update actor', res)
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 19).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['age'], 13)

    def test_failed_update_actor(self):
        res = self.client().patch('/actors/300', json={'age': 50},
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        print('failed update actor', res)
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 300).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_movie(self):
        res = self.client().patch('/movies/3', json={'release_date': 2004},
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        print('update movie', res)
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['release_date'], '2004')

    def test_failed_update_movie(self):
        res = self.client().patch('/movies/300', json={'release_date': 2000},
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 300).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


if __name__ == "__main__":
    unittest.main()

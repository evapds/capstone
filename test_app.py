import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

Casting_Assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWRlMjczNTM0NDEzNzAwMTQ5OWU0YTYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYxODAyNSwiZXhwIjoxNTkxNzA0NDI1LCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.LdYWdcvvtc2XqTdbML1iOdWT84fXf2YCR5PS_BM2lfvUmNZtzQKyUbNgq6ePDcCnUEgbhdS5A5ja_iftymf1eDtwudf8Pg5i3CgVcoRMF9PLnUZkY0jpZHiw0EXgWJTJ1AjwoSXVWUDkz9GPdzJufjXcVgCPJeCuzV-ztSyueAHJ6MnIpqmxJ53kabE8_tRC8NqrRKcstqj9rtHsOktE6D7X6SJ0ebehoMO3Xa7_EdJCxRZUxTQKlMoyUnvavg60Lk_5lLMUW9kxGCWvci0r_3hBrEe-thSZg1XAE0KgzcbZBujnzpi58_bHD7z-Ykos1NzTb4C68lNZ9rB3bNrdPA'
Casting_Director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWRlMjc4OGY4N2EyYTAwMTk5YzU5MGEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYxODA2MSwiZXhwIjoxNTkxNzA0NDYxLCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.y4AFx1FuEVfKM6Z_NR8gpz5eew_MNVoDDfOLI_rgtaSXiPs1i4vyWoEqx7Z7W8xhwd-wKFiUtuh5tvW0sjEWAnDC9gxcio3v166YbAvPa-AI8ks2rI1_jrxP8EPmUPl-b-T2uAKTpKKS3WKhSn9dQbKmf6byHxBfiajAvwZrdhH-IJ8cYx8HRMpwaDmbdk0oLn0_D41mnJTCX8tdwKCGd8NED94Pp_7BkE_HhQhVONudgu5VYeCppwBU0WihlDmsQdNQmI2Xxx6coUf8LikH94FK48eWNc2eoah-DcnEPexdy2uAfpzYDWi3tLqmx6z5ZO4KJxAForGeZ81hEH7wZg'
Executive_Producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWRlMjZmNjRlNDZhOTAwMTNjMjdmMTAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTYxNzk2MCwiZXhwIjoxNTkxNzA0MzYwLCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.nW-W2t7DqnpVGJKsqQQEc4ASV8oLpE-bucjtevBtOASjowMLcegK8SJQwlXXafYksFImgB-Nk7r4XowaJOEdBnwZC3NVdrjrMJX4QzX29MYkBt5TDIaWsMAEy6l96iUZ3Cgkpe_wGz3NHiYDh2JU4vv_Ef2C83_QL92nmdf32Idrq42w2nU_A5r6kAWZ8NfVBqB9pU9Siy8P7lcCReIzJZsTJt55Ig-I24t0W7-ONGUD2HKx3a_-dngQ40Ns8HKY0JzOmYTVoP-TizfWKXSUHsOaB3Ubu4NoYlKAXnA99ny_dqpAcKcRW16UHngxViOwq9VVzZShXBGnlbGpbL0N5Q'


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
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
            'name': 'Linda',
            'age': 53,
            'gender': 'female'
        }

        self.new_movie = {
            'title': 'Exciting new movie',
            'release_date': '2021'
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
            '/actors/1', headers={"Authorization": "Bearer " + Casting_Director})
        print(res)
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 1).one_or_none()

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
        self.assertEqual(data['message'], 'Unprocessable')

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1', headers={"Authorization": "Bearer " + Executive_Producer})
        print('delete movie', res)
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    def test_delete_movie_with_wrong_permission(self):
        res = self.client().delete(
            '/movies/2', headers={"Authorization": "Bearer " + Casting_Assistant})
        print('movie deletion wrong permission', res)
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 2).one_or_none()

        self.assertEqual(res.status_code, 401)
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
        res = self.client().patch('/actors/2', json={'name': 'Marianne'},
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        print('update actor', res)
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['name'], 'Marianne')

    def test_failed_update_actor(self):
        res = self.client().patch('/actors/300',
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        print('failed update actor', res)
        print(res.data)
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 300).one_or_none()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_update_movie(self):
        res = self.client().patch('/movies/3', json={'release_date': 2019},
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        print('update movie', res)
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['release_date'], '2019')

    def test_failed_update_movie(self):
        res = self.client().patch('/movies/300', json={'release_date': 2000},
                                  headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 300).one_or_none()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')


if __name__ == "__main__":
    unittest.main()

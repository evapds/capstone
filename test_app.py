import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

Casting_Assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYWUxMTM2OGJjNjBjMGFmMzg4ZWUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTE3NjYyNSwiZXhwIjoxNTkxMTgzODI1LCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.ckw7UIgMDB-APZFXXSI0kYSBP3fyNkdB7ENl4in1AEY1dvbdsX5iWo0lwIWdY5Uig6OvDGtOfV07qCiwoI5tZokzjsjSJZu16cs2Hhvnpf3gd3WdRLANs_2rm9dSS6tpnhI2Fno3pFDUNVnPQrli8Eo93FfQvUo6GjYZM_BroR3_F8HrZxp-DWMPO1XVvGHLCSlThWqRo-JF9Md0cQy5MdPr81s7H1M2T_F8FkRHi36YbYOWjOR1nKmVWZHGJ0KODV_TE6IG89RG6tzKhrKicpTrd5WtiIsANAw5DGw1hP1DNlmyxHnBF_UhcCcLyEIkhdJhOYjxw1mletsHZjHEgQ'
Casting_Director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYjAyOTcyODA0MTBjMWJiNWZlYWEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTE3NjY3MSwiZXhwIjoxNTkxMTgzODcxLCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.XZ340WI6uJC3WPaOS8o8AtS8AvzgToFp4GuhCBnXXi8ZtgLhtpqxHAcbcJJqC-_aJFdZvmx-nuWxHvB_tnv_7Pes2DXXzSfiTq0v3_vx6rByxhpXOXY5aX44EaoMd7Az4T2vz_OUomFHAnOLc6Uh3QgqNn9oHkCbyfSI1xFQGe4XXhv8mqyGUCLRKH3vaQw5gaZT2Q1ucTVE1QBc1AxpIOAjaWvaB9-t_XeNB39Bls7DbKfE3MNusM3jGU5aRRAYrINc9E1Y8F46jo-z5FbC5-cGlLBpX2X8PDlce3M7mgWjHumRcTjDoY3C6LsUfdN5xxA_8LTJrGFjrKoPP4iXWA'
Executive_Producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJNaTY3Y3BTaURLaEJoOUVQZmZvQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcGRzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNiYjAyOTcyODA0MTBjMWJiNWZlYWEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5MTE3Njc3MiwiZXhwIjoxNTkxMTgzOTcyLCJhenAiOiI3U2Q5eFBPOENGbnpRM0FFREg3bTlYTTRPbUx4bXprVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.IB4ddSCmoxcoQCl5MHLq35nevNGGHnaSl_XaYjxJVyYRGAdrWg9WFRQQGFnVmMfxwGeEwa8_v5qYpFosNF_4LDC4ngUnblKuzQvQTzxq-U5ffh5_QtTav4ckFWiQRk2G89c8PgxAo1O-wUV_ZLYAQ3u3Be0rkWY10o4GL4ri9TXrVtUh0Wk95sQQMzF4fjAwZjz2gwT08ZGSXsjv4SsXd7Mg0CSKTGJ_4rmPrh8jymBo_jm_VjADBa7fjXnSM5DjhicxERIZJEG-r0QmpD09OWaoDLy07-87ohzpEavg5bRGqceStciVz8EkMm5ypwSJdkJV66P-oEIr455-iH38AA'


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
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


# add permissions to endpoints
# Casting Assistant
# - Can view actors and movies
# Casting Director
# - All permissions a Casting Assistant has and…
# - Add or delete an actor from the database
# - Modify actors or movies
# Executive Producer
# - All permissions a Casting Director has and…
# - Add or delete a movie from the database

if __name__ == "__main__":
    unittest.main()

import os
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        excited = os.environ.get('EXCITED')
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return greeting

    # list of actors
    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='view:actors')
    def get_actors(payload):
        all_actors = Actors.query.all()
        actors = [actor.format() for actor in all_actors]
        return jsonify({
            'success': True,
            'actors': actors
        })

    # list of movies
    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='view:movies')
    def get_movies(payload):
        all_movies = Movies.query.all()
        movies = [movie.format() for movie in all_movies]
        return jsonify({
            'success': True,
            'movies': movies
        })

    # delete individual actors
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            result = {
                'success': True,
                'delete': id
            }
            return jsonify(result)
        except:
            abort(422)

    # delete individual movies
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, id):
        try:
            movie = Movies.query.filter(Movies.id == id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            result = {
                'success': True,
                'delete': id
            }
            return jsonify(result)
        except:
            abort(422)

    # add new actors
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='add:actors')
    def add_actors(payload):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actors(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            result = {
                'success': True,
                'created': actor.id,
                'actors': actor
            }
            return jsonify(result)
        except:
            abort(422)

    # add new movies
    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='add:movies')
    def add_movies(payload):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movies = Movies(title=new_title, release_date=new_release_date)
            movies.insert()

            result = {
                'success': True,
                'created': movies.id,
                'movies': movies
            }
            return jsonify(result)
        except:
            abort(422)

    # update existing actors
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='update:actors')
    def update_actors(payload, id):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()

            if actor is None:
                abort(404)

            actor = Actors(name=new_name, age=new_age, gender=new_gender)
            actor.update()

            result = {
                'success': True,
                'actors': actor
            }
            return jsonify(result)
        except:
            abort(422)

    # update existing movies
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='update:movies')
    def update_movies(payload, id):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movies.query.filter(Movies.id == id).one_or_none()
            if movie is None:
                abort(404)

            movie.title = new_title
            movie.title.update()

            movie.release_date = new_release_date
            movie.release_date.update()

            result = {
                'success': True,
                'movie': movie
            }
            return jsonify(result)
        except:
            abort(422)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()

# Errorhandler
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Permission not found'
    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
        'success': False,
        'error': ex.status_code,
        'message': ex.error['code']
    }), 401

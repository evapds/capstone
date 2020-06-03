import os
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from models import setup_db, Actors, Movies

from .auth.auth import AuthError, requires_auth


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

    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='view:actors')
    def get_actors():
        all_actors = Actors.query.all()
        return jsonify({
            'success': True,
            'actors': all_actors
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='view:movies')
    def get_movies():
        all_movies = Movies.query.all()
        return jsonify({
            'success': True,
            'movies': all_movies
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(id):
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

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(id):
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

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='add:actors')
    def add_actors():
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actors = Actors(name=new_name, age=new_age, gender=new_gender)
            actors.insert()

            result = {
                'success': True,
                'actors': actors
            }
            return jsonify(result)
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='add:movies')
    def add_movies():
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movies = Movies(title=new_title, release_date=new_release_date)
            movies.insert()

            result = {
                'success': True,
                'movies': movies
            }
            return jsonify(result)
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='update:actors')
    def update_actors(id):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()

            if actor is None:
                abort(404)

            actor_name = Actors(name=new_name)
            actor_name.update()

            actor_age = Actors(age=new_age)
            actor_age.update()

            actor_gender = Actors(gender=new_gender)
            actor_gender.update()

            result = {
                'success': True,
                'actors': actor
            }
            return jsonify(result)
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='update:movies')
    def update_movies(id):
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
        'message': 'Unauthorized'
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

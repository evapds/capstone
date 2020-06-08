# capstone

## Description

This project will allow me to become a graduate of the Udacity Full Stack Developer Program. I am very excited about that.
This app contains movies and actors and depending on your permission you are able to add, delete or update movies and actors.
I have learned a lot during this course and this project brought everything together. Have fun navigating through the app!

The application api is hosted via: https://capstoneepds.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/capstone` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./capstone` directory first ensure you are working using your created virtual environment.


To run the server, execute:

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## Database Setup

To import a PostgreSQL database using the psql program, follow these steps:

- Transfer the dbexport.pgsql file to your A2 Hosting account using SCP, SFTP, or FTP.
- Log in to your A2 Hosting SSH account.
- Type the following command, and then press Enter. Replace username with your username and replace dbname with the name of the database that you want to import the data into:
```psql -U username dbname < dbexport.pgsql
```
- The dbname database should now contain the data that is in the dbexport.pgsql file.

## Error Handling

Errors are returned as JSON objects in the following format:

{
    'success': False,
    'error': 400,
    'message': 'Bad request'
}

The API will return five error types when requests fail:

- 400: Bad request
- 401: Permission not found
- 404: Not found
- 422: Unprocessable
- 500: Internal Server Error

## Access Details

On the login link below you can login with the following 3 users to generate a token with the correct token.

### Login to Auth0:
https://dev-epds.eu.auth0.com/authorize?audience=capstone&response_type=token&client_id=7Sd9xPO8CFnzQ3AEDH7m9XM4OmLxmzkW&redirect_uri=http://127.0.0.1:3000/login-results

### Login details:
Casting Assistant           assistant@capstone.com         NewPassword123
Casting Director             director@capstone.com           NewPassword123
Executive Producer        producer@capstone.com         NewPassword123

## Endpoints

1. GET /actors
2. GET /movies
3. DELETE /actors/
4. DELETE /movies/
5. POST /actors/
6. POST/movies/
7. PATCH /actors/
8. PATCH /movies/

## Roles
There are 3 roles in the project: Casting Assistant, Casting Director, and Executive Producer

Here is the permission table for each role:

### Casting Assistant:

GET /actors
GET /movies

### Casting Director:

GET /actors
GET /movies
DELETE /actors/
POST /actors/
PATCH /actors/
PATCH /movies/

### Executive Producer:

GET /actors
GET /movies
DELETE /actors/
DELETE /movies/
POST /actors/
POST/movies/
PATCH /actors/
PATCH /movies/

## Tests

Tests have been implemented using unit test.
There is one successful (success=true) and one faulty (success=false) test case for each api in the test_app.py. 
In order to run the test, run:

```
python test_app.py
```

## Author
Very proud author, Eva Parth dos Santos

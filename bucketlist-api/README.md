# bucketlist-api

[![Build Status](https://travis-ci.org/inno-asiimwe/bucketlist-api.svg?branch=master)](https://travis-ci.org/inno-asiimwe/bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/inno-asiimwe/bucketlist-api/badge.svg?branch=master)](https://coveralls.io/github/inno-asiimwe/bucketlist-api?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/20719403902bf7b679c5/maintainability)](https://codeclimate.com/github/inno-asiimwe/bucketlist-api/maintainability)

## Technologies used 
1. Python
2. Flask
3. Postgresql
4. Nosetest
5. Swagger

## How to install
1. Clone repository
2. Install dependencies
```pip install -r requirements.txt```
3. Make sure PostgreSQL server is installed and running
4. create database
```$ psql --user postgres```
```postgres=# create database flask_api;```
3. Initialise db and run migrations to create the necessary tables
```manage.py db init```
```manage.py db migrate```
```manage.py db upgrade```
4. Run application using 
```python run.py```

## Features implemented
* User registration
* User login and logout
* Bucketlist creation, editing and deletion
* Bucketlist item creation, editing and deletion
* Search by bucketlist by name
* pagination of results

## Running Tests
   ``` nosetests ```

## Heroku link
        https://inno-bucketlist-api.herokuapp.com

## Documentation 
        http://127.0.0.1:5000/apidocs/
        https://inno-bucketlist-api.herokuapp.com/apidocs/



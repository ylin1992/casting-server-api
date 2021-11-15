# Casting-Agency API
The project provides a backend service where users are allowed to add, delete, check and modify actors and movies based on their authorities.
1. The service and database are hosted on Heroku, the base endpoint is [https://casting-api-elin92.herokuapp.com](https://casting-api-elin92.herokuapp.com)
2. The authentication is provided by Auth0, for more detail, please refer to [Authentication](#Authentication) session.
3. The app can also run on local server, for more detail, please refer to [Running on local server](#Running-on-local-server) session.

# API References

## Authentication
The API is hosted by an athentication basis, which means all operations and requests have to be bundled with an authorized token

### Authorization
There are 3 level of authority:
- **Assistant**: 
    - Can view information of actors and movies
- **Director**: 
    - Can delete an actor and modify actor list of a movie
    - All permissions assistant has
- **Producer**:
    - Can add or delete a movie
    - All permissions director has

### Get a token
1. Visit [login URL](https://dev-artpgixt.us.auth0.com/authorize?audience=casting-api&response_type=token&client_id=vrDoSPpPqVtxnIRlOQDk7FH8UJsTSPLB&redirect_uri=https://casting-api-elin92.herokuapp.com/callback)
2. Login with your user email and password (or sign up a new user account)
3. If your login is complete, your will be redireced to a page showing your web token
4. Copy your web token for your future reuqests

### Notice
1. The token will be valid for 1 day, be sure to login again to extend your permissions.
2. By default, you **will not be granted any permissions**, contact us to get your account upgraded.

## Base URL 
The app is hosted on Heroku, base url: [https://casting-api-elin92.herokuapp.com](https://casting-api-elin92.herokuapp.com)

## Endpoints - Actors

### GET /actors
- General: Returns all actors, a success flag and number of total actors.
- Authorization: Assistant, Director, Producer
- Example: 
```
curl https://casting-api-elin92.herokuapp.com/actors \
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "actors": [
        {
            "age": 30,
            "gender": "M",
            "id": 11,
            "movies": [
                7
            ],
            "name": "a3"
        },
        ...
        {
            "age": 18,
            "gender": "M",
            "id": 14,
            "movies": [],
            "name": "The Very First Actor"
        }
    ],
    "success": true,
    "total_actors": 5
}
```

### GET /actors/<int: actor_id>
- General: Returns actor with the input id and a success flag.
- Authorization: Assistant, Director, Producer
- Example: 
```
curl https://casting-api-elin92.herokuapp.com/actors/11
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "actor": {
        "age": 30,
        "gender": "M",
        "id": 11,
        "movies": [
            7
        ],
        "name": "a3"
    },
    "success": true
}
```
- Errors:
    - 404: No actor with the input id

### GET /actors/<int: actor_id>/movies
- General: Returns movies that the actor with the input id particpates in
- Authorization: Assistant, Director, Producer
- Example: 
```
curl https://casting-api-elin92.herokuapp.com/actors/11/movies
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "movies_id": [
        7
    ],
    "success": true,
    "total_movies": 1
}
```
- Errors:
    - 404: No actor with the input id

### POST /actors
- General: Creates a new actor into the database
    - Input: JSON format:
    ```
    {
        "name": "actor's name",
        "age": actor's age (in integer),
        "gender": actor's gender ("m", "M", "f", "F")
    }
    ```
    - Return: Info of created actor
- Authorization: Director, Producer
- Example: 
```
curl -X POST https://casting-api-elin92.herokuapp.com/actors \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer {YOUR_TOKEN}' \
     -d '{"name": "A new actor","age": 11,"gender": "m"}'```
```
```
{
    "create": {
        "age": 11,
        "gender": "M",
        "id": 15,
        "movies": [],
        "name": "A new actor"
    },
    "success": true
}
```
- Errors:
    - 400: Invalid request including:
        - Invalid gender, i.e. ```"X"```, ```""```, ```1```
    - 422: Unprocessable input:
        - Invalid name: ```123```
        - Invalid age: ```"One Year Old"```

### PATCH /actors/<int: actor_id>
- General: Modify an existing actor in the database by the given id
    - Input: JSON format (not all fields are neccessary):
    ```
    {
        "name": "actor's name",
        "age": actor's age (in integer),
        "gender": actor's gender ("m", "M", "f", "F"),
        "movies": an array of movie id the actor participates in
    }
    ```
    - Return: Info of modified actor
- Authorization: Director, Producer
- Example: 
```
curl -X PATCH https://casting-api-elin92.herokuapp.com/actors/ \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer {YOUR_TOKEN}' \
     -d '{"name": "modified name","age": 11, "movies": [8,9,10]}'```
```
```
{
    "actor": {
        "age": 30,
        "gender": "M",
        "id": 11,
        "movies": [
            8,
            9,
            10
        ],
        "name": "modified name"
    },
    "success": true
}
```
Now if we check movie #8, we can find that actor #11 is added into movie #8's "actors" field
```
curl https://casting-api-elin92.herokuapp.com/actors/8
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "movie": {
        "actors_id": [
            9,
----------->11
        ],
        "id": 8,
        "release_date": "Wed, 22 May 2019 21:30:00 GMT",
        "title": "m2"
    },
    "success": true
}
```
- Errors:
    - 400: Invalid request including:
        - Invalid gender, i.e. ```"X"```, ```""```, ```1```
        - Movie with movie id can not be found
    - 422: Unprocessable input:
        - Invalid name: ```123```
        - Invalid age: ```"One Year Old"```
    - 404: 
        - actor with input id is not found

### DELETE /actors/<int: actor_id>
- General: Delete an actor with the given id and return the deleted id
    - Note: If the actor is in the list of certain movies' "actors" list, the actor will be automatically removed from them.
- Authorization:  Director, Producer
- Example: Delete actor #11
```
curl -X DELETE https://casting-api-elin92.herokuapp.com/actors/11 \
     -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "delete": 11,
    "success": true
}
```
Now we get ```/movie/8``` (where it contained ***actor #8*** but now has been removed)
```
{
    "movie": {
        "actors_id": [
            9
        ],
        "id": 8,
        "release_date": "Wed, 22 May 2019 21:30:00 GMT",
        "title": "m2"
    },
    "success": true
}
```
- Errors:
    - 404: No actor with the input id

## Endpoints - Movies
### GET /movies
- General: Returns all movies, a success flag and number of total movies.
- Authorization: Assistant, Director, Producer
- Example: 
```
curl https://casting-api-elin92.herokuapp.com/movies \
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "movies": [
        {
            "actors_id": [
                9
            ],
            "id": 8,
            "release_date": "Wed, 22 May 2019 21:30:00 GMT",
            "title": "m2"
        },
        ...
        {
            "actors_id": [
                9,
                12
            ],
            "id": 7,
            "release_date": "Sat, 23 May 2020 21:30:00 GMT",
            "title": "A great movie"
        }
    ],
    "success": true,
    "total_movies": 8
}
```

### GET /movies/<int: movie_id>
- General: Returns movie with the input id and a success flag.
- Authorization: Assistant, Director, Producer
- Example: 
```
curl https://casting-api-elin92.herokuapp.com/movies/11
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "movie": {
        "actors_id": [
            9,
            12
        ],
        "id": 7,
        "release_date": "Sat, 23 May 2020 21:30:00 GMT",
        "title": "modified title"
    },
    "success": true
}
```
- Errors:
    - 404: No movie with the input id is found

### GET /movies/<int: actor_id>/actors
- General: Returns all actors in the movie with the given movie id
- Authorization: Assistant, Director, Producer
- Example: 
```
curl https://casting-api-elin92.herokuapp.com/movies/8/actors \
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "actors_id": [
        9
    ],
    "success": true,
    "total_actors": 1
}
```
- Errors:
    - 404: No movie with the input id is found

### POST /movies
- General: Creates a new movie into the database
    - Input: JSON format:
    ```
    {
        "title": "movie's title",
        "release_date": "datetime without time zone " (follow "YYYY-MM-DDTHH:MM:SS.000Z format" or "YYYY/DD/MM")
    }
    ```
    - Return: Info of created movie
- Authorization: Producer
- Example: 
```
curl -X POST https://casting-api-elin92.herokuapp.com/movies \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer {YOUR_TOKEN}' \
    -d '{"title":"A great movie", "release_date":"2019-05-23T21:30:00.000Z"}'
```
```
{
    "create": {
        "actors_id": [],
        "id": 2,
        "release_date": "Thu, 23 May 2019 21:30:00 GMT",
        "title": "A great movie"
    },
    "success": true
}
```
- Errors:
    - 422: Unprocessable input:
        - Invalid release_date: ```"-05-23T21:30:00.000Z"```, ```12345```
        - Invalid title: ```12```

### PATCH /movies/<int: movie_id>
- General: Modify an existing movie in the database by the given id
    - Input: JSON format (not all fields are neccessary):
    ```
    {
        "title": "movie's title",
        "release_date": "valid timestamp",
        "actors": an array of actor id participating in this movie
    }
    ```
    - Return: Info of modified actor
- Authorization: Director, Producer
- Example: 
```
curl -X PATCH https://casting-api-elin92.herokuapp.com/actors/ \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer {YOUR_TOKEN}' \
     -d '{"title":"Modified title", "release_date":"2021.05.08", "actors":[3,5,6]}''
```
```
{
    "movie": {
        "actors_id": [3, 5, 6],
        "id": 1,
        "release_date": "Sat, 08 May 2021 00:00:00 GMT",
        "title": "Modified title"
    },
    "success": true
}
```
Now if we check movie #3 or #5 or #6, we can find that movie #1 is added into movie their "actors" field
```
curl https://casting-api-elin92.herokuapp.com/actors/1
    -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "actor": {
        "age": 108,
        "gender": "m",
        "id": 3,
        "movies": [
----------->1
        ],
        "name": "An actor"
    },
    "success": true
}
```
- Errors:
    - 422: Unprocessable input:
        - Invalid release_date: ```"-05-23T21:30:00.000Z"```, ```12345```
        - Invalid title: ```12```
    - 404: 
        - movie with input id is not found


### DELETE /movies/<int: movie_id>
- General: Delete an movie with the given id and return the deleted id
    - Note: If the movie is in the list of certain actors' "movies" list, the movie will be automatically removed from list.
- Authorization:  Producer
- Example: Delete movie #1
```
curl -X DELETE https://casting-api-elin92.herokuapp.com/movies/1 \
     -H 'Authorization: Bearer {YOUR_TOKEN}'
```
```
{
    "delete": 1,
    "success": true
}
```
Now we get ```/actor/3``` (where it contained ***movie #1*** but now has been removed)
```
{
    "actor": {
        "age": 108,
        "gender": "m",
        "id": 3,
------->"movies": [],
        "name": "An actor"
    },
    "success": true
}
```
- Errors:
    - 404: No actor with the input id


## Error handling
Errors are returned in JSON format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API supports 6 types of status code
- 404: Data not found
- 422: Unproccessable
- 400: Bad request
- 401: Unauthorized
- 403: Invalid token
- 500: Internal error

# Running on local server
The app can be hosted locally, several steps should be completed before moving on.
1. **Install Python 3.7**: Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **PIP Dependencies** - Install dependencies by naviging to the root directory and running:
```bash
pip install -r requirements.txt
```

3. **Setup Environment Variables** - Open the "setup_local.sh" file and fill in the following part
```
export TEST_ASSISTANT_TOKEN='<ASSISTANT_TOKEN>'
export TEST_DIRECTOR_TOKEN='<DIRECTOR_TOKEN>'
export TEST_PRODUCER_TOKEN='<PRODUCER_TOKEN>'
export DB_HOST='<YOUR_SECRET_DB_HOST_NAME>'
export DB_USER='<YOUR_USER_NAME>'
export DB_PWD='<YOUR_DB_PWD>'
```
**Note**: 
    - The three tokens mentioned above have to be granted by Auth0 server
    - The default db is postgres SQL

After the bash file is complete, run the command to setup your environment:
```
source setup_local.sh
```
**Note**: In the bash file, there is a casting_test database created for unit tests, if you are not going to run unit test, it is fine to skip the step

4. **Migrate Database**: run the following script to create neccessary tables.
```
python migrate.py db upgrade
```
After running the script, check the result in ```psql```, it might look like:
```
psql casting
casting=# \dt
            List of relations
 Schema |      Name       | Type  | Owner 
--------+-----------------+-------+-------
 public | Actor           | table | <your_user_name>
 public | Gender          | table | <your_user_name>
 public | Movie           | table | <your_user_name>
 public | actors_movies   | table | <your_user_name>
 public | alembic_version | table | <your_user_name>
 public | gender_actors   | table | <your_user_name>
(6 rows)
```

5. **Launch The Program**: Navigate to the root directory and run
```
python app.py
```

6. **Start Using API**: The port is by default hosted on ```port:5000```, base URL: [http://loalhost:5000](http://loalhost:5000)

## (Optional) Run unitest
There are 3 test files in the ```/tests``` directory.
- ```test_auth.py```: tests errors about authentication
- ```test_actor_routes.py```: tests actor routes' functionality
- ```test_movie_routes.py```: tests movie routes' functionality

### Run single test
If you are going to run a single test, run below commands:
```
python -m tests.test_auth           # run authentication test
python -m tests.test_actor_routes   # run actor routes test
python -m tests.test_movie_routes   # run movie routes test
```

### Run all test
If you are going to run all tests, run below commands:
```
python -m unittest discover
```
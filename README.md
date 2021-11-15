# Casting-Agency API
The project provides a backend service where users are allowed to add, delete, check and modify actors and movies based on their authorities.
1. The service and database are hosted on Heroku, the base endpoint is [https://casting-api-elin92.herokuapp.com](https://casting-api-elin92.herokuapp.com)
2. The authentication is provided by Auth0, for more detail, please refer to "Authentication" session.
3. The app can also run on local server, for more detail, please refer to "Running on local server" session.

## API References

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

## Base URL: [https://casting-api-elin92.herokuapp.com](https://casting-api-elin92.herokuapp.com)

## Endpoints

### GET /actors
- General: Returns all actors, a success flag and number of total actors.
- Authorization: Assistant, Director, Producer
- Example: ```curl https://casting-api-elin92.herokuapp.com/actors```
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
- Example: ```curl https://casting-api-elin92.herokuapp.com/actors/11```
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
- Example: ```curl https://casting-api-elin92.herokuapp.com/actors/11/movies```
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
```curl -X PATCH https://casting-api-elin92.herokuapp.com/actors/ \
                   -H 'Content-Type: application/json' \
                   -H 'Authorization: Bearer {YOUR_TOKEN}' \
                   -d '{"name": "modified name","age": 11, "movies": [8,9,10]}'```
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
Now if we check movie #8, we can find that actor #11 is added into movie #8's "actors" field
```curl https://casting-api-elin92.herokuapp.com/actors/8```
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
```curl -X POST https://casting-api-elin92.herokuapp.com/actors \
                   -H 'Content-Type: application/json' \
                   -H 'Authorization: Bearer {YOUR_TOKEN}' \
                   -d '{"name": "A new actor","age": 11,"gender": "m"}'```
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

### DELETE /actors/<int: actor_id>

## Error handling
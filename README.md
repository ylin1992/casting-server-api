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
- Example: 

### GET /actors/<int: actor_id>

### GET /actors/<int: actor_id>/movies

### POST /actors

### PATCH /actors/<int: actor_id>

### DELETE /actors/<int: actor_id>

## Error handling
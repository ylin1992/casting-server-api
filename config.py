import os
def modify_database_url(database_path):
    if database_path is None:
        return None
    db_path_parts = database_path.split('://')
    return db_path_parts[0] + 'ql://' + db_path_parts[1]


SQLALCHEMY_DATABASE_URI = ''
DEV_LEVEL = os.getenv('DEV_LEVEL', 'DEV')

if DEV_LEVEL == 'LOCAL':
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PWD  = os.getenv('DB_PWD', 'postgres')
    DB_NAME = os.getenv('DB_NAME', 'casting')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_NAME)
else:
    database_path = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = modify_database_url(database_path)
    

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'dev-artpgixt.us.auth0.com')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE', 'casting-api')
AUTH_INFO = {
    'AUTH0_DOMAIN': AUTH0_DOMAIN,
    'ALGORITHMS': ALGORITHMS,
    'API_AUDIENCE': API_AUDIENCE
}
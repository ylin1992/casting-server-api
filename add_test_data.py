from database.models import Actor, Movie, Gender, db

def add_gender():
    genders = Gender.query.all()
    if (genders is None) or len(genders) == 0:
        male = Gender(id=1, name='M')
        female = Gender(id=2, name='F')
        male.insert()
        female.insert()

def sample_movie():
    return [
        {
            "title": 'm1',
            "release_date": '2019-05-21T21:30:00.000Z',
        },
        {
            "title": 'm2',
            "release_date": '2019-05-22T21:30:00.000Z',
        },
        {
            "title": 'm3',
            "release_date": '2019-05-23T21:30:00.000Z',
        },
        {
            "title": 'm4',
            "release_date": '2019-05-23T21:30:00.000Z',
        },
        {
            "title": 'm5',
            "release_date": '2019-05-21T21:30:00.000Z',
        },
        {
            "title": 'm6',
            "release_date": '2019-05-22T21:30:00.000Z',
        },
        {
            "title": 'm7',
            "release_date": '2019-05-23T21:30:00.000Z',
        },
        {
            "title": 'm8',
            "release_date": '2019-05-23T21:30:00.000Z',
        },
    ]

def sample_actors():
    return [
        {
            "name": 'a1',
            "age": 10,
            "gender_id": 1
        },
        {
            "name": 'a2',
            "age": 20,
            "gender_id": 2
        },
        {
            "name": 'a3',
            "age": 30,
            "gender_id": 1
        }]
    
if __name__ == '__main__':
    from app import app
    with app.app_context():
        add_gender()
        
        Actor.query.delete()
        Movie.query.delete()
        for a in sample_actors():
            actor = Actor(name=a['name'],
                          age=a['age'],
                          gender_id=a['gender_id'])
            actor.insert()
        
        for m in sample_movie():
            movie = Movie(title=m['title'],
                          release_date=m['release_date'])
            movie.insert()
        
        # add relationship
        actors = Actor.query.all()
        movies = Movie.query.all()
        movie1 = movies[0]
        movie1.actors.append(actors[0])
        movie1.actors.append(actors[1])
        movie2 = movies[1]
        movie2.actors.append(actors[0])
        movie2.actors.append(actors[1])
        db.session.commit()
        print(actors[0].movies)

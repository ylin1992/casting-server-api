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
            "id": 1,
            "title": 'm1',
            "release_date": '2019-05-21T21:30:00.000Z',
        },
        {
            "id": 2,
            "title": 'm2',
            "release_date": '2019-05-22T21:30:00.000Z',
        },
        {
            "id": 3,
            "title": 'm3',
            "release_date": '2019-05-23T21:30:00.000Z',
        },
    ]

def sample_actors():
    return [
        {
            "id":1,
            "name": 'a1',
            "age": 10,
            "gender_id": 1
        },
        {
            "id":2,
            "name": 'a2',
            "age": 20,
            "gender_id": 2
        },
        {
            "id":3,
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
            actor = Actor(id=a['id'],
                          name=a['name'],
                          age=a['age'],
                          gender_id=a['gender_id'])
            actor.insert()
        
        for m in sample_movie():
            movie = Movie(id=m['id'],
                          title=m['title'],
                          release_date=m['release_date'])
            movie.insert()
        
        # add relationship
        movie1 = Movie.query.get(1)
        movie1.actors.append(Actor.query.get(1))
        movie1.actors.append(Actor.query.get(2))
        movie2 = Movie.query.get(2)
        movie2.actors.append(Actor.query.get(1))
        movie2.actors.append(Actor.query.get(3))
        db.session.commit()
        print(Actor.query.get(1).movies)

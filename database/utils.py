from database.models import Gender

def get_gender_from_string(string):
    # gender must be one of 'f', 'F', 'm', 'M'

    if string is None:
        return None
    gender = Gender.query.filter(Gender.name.ilike(string)).one_or_none()
    print('gender: ', gender)
    return gender

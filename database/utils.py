from database.models import Gender

def get_gender_from_string(string):
    # gender must be one of 'f', 'F', 'm', 'M'
    print('string: ', string)
    print('type(string) ', type(string))
    print('len(string) ', len(string))
    if string is None:
        return None

    if type(string) is not str:
        return None
    
    if len(string) == 0:
        return None
    gender = Gender.query.filter(Gender.name.ilike(string)).one_or_none()
    return gender

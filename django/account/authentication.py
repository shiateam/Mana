import datetime , jwt

def create_access_token(id):
    return jwt.encone({
       'user_id': id,
       'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
       'iat': datetime.datetime.utcnow() 
    }, 'access_secret' , algorithm = 'HS256')


def create_refresh_token(id):
    return jwt.encone({
       'user_id': id,
       'exp':datetime.datetime.utcnow() + datetime.timedelta(days = 7),
       'iat': datetime.datetime.utcnow() 
    }, 'access_secret' , algorithm = 'HS256')
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt



SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 5


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=5)

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get('sub')

        if email is None:
            raise credentials_exception

        token_data = {
            'email': email,
            'name': payload.get('name')
        }

        return token_data

    except JWTError:
        raise credentials_exception


def get_token_username(request, credentials_exception):
    if 'ap-login' in request.cookies.keys():
        if request.cookies['ap-login']:
            return verify_token(request.cookies['ap-login'], credentials_exception)['name']

    return 'Guest'



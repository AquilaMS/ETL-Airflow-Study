import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

class AuthHandler():
    security =  HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")
    secret = 'a secret key'
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    #return a bool | compare insert password to the encrypted password 
    def verify_password(self, no_hash_password, hashed_password):
        print(self.pwd_context.verify(no_hash_password, hashed_password))
        return self.pwd_context.verify(no_hash_password, hashed_password) 

    #encode into JWT using secret key
    def encode_token(self, user_id):
        payload = {
            'sub': user_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')
    #decode JWT using secret key
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            return payload['sub']
        except jwt.InvalidTokenError as error:
            raise HTTPException(status_code=401, detail='Invalid Token')

    #prevents dependencies injections 
    def auth_wrapper(self, auth:HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

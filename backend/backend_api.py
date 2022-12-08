from fastapi import FastAPI, Depends, HTTPException
import fastapi.security
from database import engine, SessionLocal
from sqlalchemy.orm import Session 
import models
import schemas 
from auth.auth import AuthHandler

app = FastAPI() 

models.Base.metadata.create_all(bind = engine)

admins = []
auth_handler = AuthHandler()

#fake admin account
system_admin = schemas.AuthSchema(
    username =  'admin',
    password = 'admin'
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def auto_admin_register(auth_schema: schemas.AuthSchema):
    hashed_password = auth_handler.get_password_hash(auth_schema.password)
    admins.append({
        'username': auth_schema.username,
        'password': hashed_password
    })
    return

@app.post('/add')
def create_user_test (user: schemas.User, db: Session = Depends(get_db), username = Depends(auth_handler.auth_wrapper)):
    user_model =  models.Users()
    user_model.user_id = user.user_id
    user_model.name = user.name
    user_model.email = user.email
    user_model.gender = user.gender
    user_model.phone =  user.phone
    user_model.city = user.city
    user_model.timestamp = user.timestamp
    db.add(user_model)
    db.commit()

    return username

@app.get('/getallusers')
def read_api(db: Session = Depends(get_db), username = Depends(auth_handler.auth_wrapper)):
    return db.query(models.Users).all()

@app.post('/login')
def login(auth_schema: schemas.AuthSchema):
    auto_admin_register(system_admin) #create a admin account on start
    actual_admin = None
    #verify if the 'username' is a admin's username
    for admin in admins:
        if admin['username'] == auth_schema.username:
            actual_admin = admin
            break
    #verify if the password matchs to admin's password or username is invalid
    if (actual_admin is None) or (not auth_handler.verify_password(auth_schema.password, actual_admin['password'])):
        raise HTTPException(status_code=401, detail= 'Wrong password/username')
    token = auth_handler.encode_token(actual_admin['username'])
    return token

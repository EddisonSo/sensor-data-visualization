import functools
from flask import request
from sqlalchemy.orm import Session
from domain.repositories.user_repository import UserRepository 
from domain.models.user import User
from domain.repo_exceptions import *
from ismart_api.engine import engine
from datetime import datetime
from uuid import UUID
import pytz

def is_valid(api_key):
    try: 
        UUID(api_key)
    except:
        return False 
    with Session(engine) as session:
        user_repository = UserRepository(session)
        user = user_repository.get_user(api_key)
        expiration = user.get_expiration()

        if expiration is None or expiration >= datetime.utcnow().replace(tzinfo=pytz.UTC):
            return True 

        return False
    

def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.json and request.json.get("api_key"):
            api_key = request.json.get("api_key")
        else:
            return {"message": "Please provide an API key"}, 400
        # Check if API key is correct and valid
        if is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403
    return decorator

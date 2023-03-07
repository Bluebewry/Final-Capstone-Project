from flask import request
from .models import User 




def basic_auth_required(func):

    def decorated():
        data = request.json

        username = data['username']
        password = data['password']

        user = User.query.filter_by(username = username)
        if user:
            if user.password == password:


                func()
    return decorated






def token_auth_required():
    pass

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask import app

import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')




class Users:
    def __init__(self,data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len (user['password']) <= 7:
            flash("Password must be 8 characters long")
            is_valid = False
        if len (user['first_name'])<=2:
            flash("first name must be at least 2 characters long")
            is_valid = False
        if len (user['last_name'])<=2:
            flash("last name must be at least 2 characters long")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email")
            is_valid = False
        if user['password']!= user['confirm_password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid
        

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (first_name,last_name,email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL ("appointments").query_db(query,data)
        

    @classmethod
    def login_user(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results =  connectToMySQL ("appointments").query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])


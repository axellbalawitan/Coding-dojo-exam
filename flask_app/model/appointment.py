from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime


class Appointments:
    def __init__(self,data):
        self.id = data ['id']
        self.user_id = data ['user_id']
        self.task = data ['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']


    @classmethod
    def add_appointment(cls, data):
        query = "INSERT INTO appointment (user_id,date,task,status,created_at,updated_at) VALUES (%(user_id)s,%(date)s,%(task)s,%(status)s,NOW(),NOW())"
        print (query)
        return connectToMySQL ("appointments").query_db(query,data)

    
    @classmethod
    def all_appointments(cls):
        query = "SELECT * FROM appointment;"
        results = connectToMySQL("appointments").query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts

    @classmethod
    def delete_appointment(cls, data):
        query = "DELETE FROM appointment WHERE id = %(id)s;"
        print(query)
        return connectToMySQL("appointments").query_db(query, data)

    @classmethod # for retrieval in update function
    def retrieve_appointment(cls, data):
        query = "SELECT * FROM appointment WHERE id = %(id)s;"
        results = connectToMySQL("appointments").query_db(query, data)
        if len(results) < 1 :
            return  False
        return cls(results[0])

    @classmethod # We will now be retrieving data from controller.py
    def update_appointment(cls, data):
        query = "UPDATE appointment SET user_id = %(user_id)s, task = %(task)s, date = %(date)s, status = %(status)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL("appointments").query_db(query, data)


    @staticmethod
    def validate_appointment(appointment):
        is_valid = True
        if len (appointment['date']) <= datetime.today:
            flash("You can't create appointments in the past!")
            is_valid = False
        return is_valid
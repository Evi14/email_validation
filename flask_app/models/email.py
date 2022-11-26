from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Email:

    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES ( %(email)s , NOW() , NOW());"
        return connectToMySQL('email_valid_schema').query_db( query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        results = connectToMySQL('email_valid_schema').query_db(query)
        emails = []
        for email in results:
            emails.append(cls(email))
        data = connectToMySQL('email_valid_schema').query_db(" select email from emails order by id desc limit 1;")
        flash(f"The email address you entered {data[0]['email']} is a valid email address! Thank You!" , 'emailSuccessful')
        return emails
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL('email_valid_schema').query_db( query, data )

    @staticmethod
    def is_valid(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']): 
            flash("Invalid email address!", "email")
            is_valid = False
        query = "select count(email) from emails where email = %(email)s;"
        result = connectToMySQL('email_valid_schema').query_db(query,email)
        if result[0]['count(email)'] >= 1:
            flash("This email address already exists!", "emailExists")
            is_valid = False
        return is_valid
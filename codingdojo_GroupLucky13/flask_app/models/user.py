from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    DB = 'cachemap'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Input: Nothing
    # Output: List of class objects with user information
    @classmethod
    def get_all_users(cls):
        query = """
        SELECT * 
        FROM users
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    # Input: Email address
    # Output: Class object with user information
    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    # Input: User information
    # Output: User id
    @classmethod
    def save_user(cls, data ):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: User information
    # Output: Boolean of whether or not user information is valid
    @staticmethod
    def validate_user_register(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'registration_error')
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters long!", 'registration_error')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters long!", 'registration_error')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long!", 'registration_error')
            is_valid = False
        if User.get_user_by_email(data):
            flash("Email address is already in use!", 'registration_error')
            is_valid = False
        return is_valid

    # Input: Unparsed registration data
    # Output: Parsed registration data
    @staticmethod
    def parse_user_register(data):
        parsed_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': data['password']
        }
        return parsed_data

    # Input: Unparsed login data
    # Output: Parsed login data
    @staticmethod
    def parse_user_login(data):
        parsed_data = {
            'email': data['email'],
            'password': data['password']
        }
        return parsed_data
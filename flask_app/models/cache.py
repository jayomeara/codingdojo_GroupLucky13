from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import comment
from flask_app.models import user
from flask import flash

class Cache:
    DB = 'cachemap'
    def __init__( self , data ):
        self.id = data['id']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.comments = []

    # Input: Nothing
    # Output: List of class objects with information
    @classmethod
    def get_all_caches(cls):
        query = """
        SELECT * 
        FROM caches
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        caches = []
        for cache in results:
            caches.append( cls(cache) )
        return caches

    # Input: Nothing
    # Output: List of caches, not class objects
    @classmethod
    def get_all_caches_JSON(cls):
        query = """
        SELECT * 
        FROM caches
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        caches = []
        for cache in results:
            caches.append(cache)
        return caches

    # Input: User id 
    # Output: List of class objects with information
    @classmethod
    def get_all_caches_by_user(cls, data):
        query = """
        SELECT * 
        FROM caches 
        WHERE user_id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        caches = []
        for cache in results:
            caches.append( cls(cache) )
        return caches

    # Input: Cache id 
    # Output: Single class object
    @classmethod
    def get_cache_by_id(cls, data):
        query = """
        SELECT * 
        FROM caches 
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Input: Cache id 
    # Output: Single class object w/ arrays of comments & users attached to comments
    @classmethod
    def get_cache_by_id_with_comments(cls, data):
        query = """
        SELECT * 
        FROM caches 
        LEFT JOIN comments ON comments.cache_id = caches.id
        LEFT JOIN users ON users.id = comments.user_id
        WHERE caches.id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        else:
            cache = cls(results[0])

            for row in results:
                #Create new comment instance from row data
                comment_data = {
                    'id' : row['comments.id'],
                    'message' : row['message'],
                    'created_at' : row['comments.created_at'],
                    'updated_at' : row['comments.updated_at'],
                    'user_id' : row['comments.user_id'],
                    'cache_id' : row['comments.cache_id']
                }
                cache_Comment = comment.Comment(comment_data)

                #Create new user instance from row data
                author_data = {
                    'id' : row['users.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                author = user.User(author_data)

                #Attach user instance to the comment instance through author
                cache_Comment.author = author

                #Add Comment w/author to Array of comments
                cache.comments.append(cache_Comment)
        #Return cache instance w/ array of comments w/ users
        return cache
    
    
    # Input: Cache information
    # Output: Cache id
    @classmethod
    def save_cache(cls, data ):
        query = """
        INSERT INTO caches (latitude, longitude, description, user_id) 
        VALUES (%(latitude)s, %(longitude)s, %(description)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: Cache id & Cache information
    # Output: Nothing
    @classmethod
    def update_cache(cls, data ):
        query = """
        UPDATE caches 
        SET latitude = %(latitude)s, longitude = %(longitude)s, description = %(description)s 
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: Cache id
    # Output: 
    @classmethod
    def delete_cache(cls, data ):
        query = """
        DELETE FROM caches 
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )
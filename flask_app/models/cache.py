from flask_app.config.mysqlconnection import connectToMySQL
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

    # Input: User id 
    # Output: List of class objects with information
    @classmethod
    def get_all_caches_by_user(cls):
        query = """
        SELECT * 
        FROM caches 
        WHERE user_id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        caches = []
        for cache in results:
            caches.append( cls(cache) )
        return caches

    # Input: User id 
    # Output: Single class object
    @classmethod
    def get_cache_by_id(cls):
        query = """
        SELECT * 
        FROM caches 
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        if len(results < 1):
            return False
        return cls(results[0])
    
    # Input: Cache information
    # Output: Cache id
    @classmethod
    def save_cache(cls, data ):
        query = """
        INSERT INTO caches (latitude, longitude, description, user_id)
        VALUES (%(latitude)s, %(longitude)s, %(description)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: Cache information
    # Output: Nothing
    @classmethod
    def update_cache(cls, data ):
        query = """
        UPDATE caches SET latitude = %(latitude)s, longitude = %(longitude)s, description = %(description)s, user_id = %(user_id)s
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
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    DB = 'cachemap'
    def __init__( self , data ):
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.cache_id = data['cache_id']
        self.author = None

    # Input: Cache id 
    # Output: List of class objects with information
    @classmethod
    def get_all_comments_by_cache(cls, data):
        query = """
        SELECT *
        FROM comments
        JOIN users
        ON users.id = comments.user_id
        WHERE comments.cache_id = %(id)s;
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        comments = []
        if not results:
            return comments
        for i in  range(len(results)):
            author = {
                'user_id': results[i]['users.id'],
                'first_name': results[i]['first_name'],
                'last_name': results[i]['last_name'],
            }
            comments.append(cls(results[i]))
            comments[i].author = author
        return comments

    # Input: Comment information
    # Output: Comment id
    @classmethod
    def save_comment(cls, data ):
        query = """
        INSERT INTO comments (message, user_id, cache_id) 
        VALUES (%(message)s, %(user_id)s, %(cache_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: Comment id & Comment information
    # Output: Nothing
    @classmethod
    def update_comment(cls, data ):
        query = """
        UPDATE comments 
        SET message = %(message)s 
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: Comment id
    # Output: 
    @classmethod
    def delete_comment(cls, data ):
        query = """
        DELETE FROM comments 
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )
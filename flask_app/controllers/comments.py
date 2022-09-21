from flask_app import app
from flask import render_template, redirect, request, session, flash

# Import classes
from flask_app.models.comment import Comment
from flask_app.models.cache import Cache

@app.route('/view/cache/<int:cache_id>')
def view_with_comments(cache_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : cache_id
        }
        Comment.get_all_comments_by_cache(data)
        comments=Cache.get_cache_by_id_with_comments(data)
        return render_template('cache_with_comments.html', comments=comments)


# @app.route('/postcomment', methods=['POST'])

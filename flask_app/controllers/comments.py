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
        cache = Cache.get_cache_by_id(data)
        comments = Comment.get_all_comments_by_cache(data)
        return render_template('cache_with_comments.html', comments=comments, cache=cache)

@app.route('/add_comment/<int:cache_id>', methods=['POST'])
def add_comment(cache_id):
    data = {
        'message' : request.form['message'],
        'cache_id' : cache_id,
        'user_id' : request.form['user_id']
    }
    Comment.save_comment(data)
    return redirect(f'/view/cache/{cache_id}')


@app.route('/delete/comment/<int:comment_id>/<int:cache_id>/<int:user_id>')
def delete_comment(comment_id, cache_id, user_id):
    if user_id != session['user_id']:
        return redirect (f'/view/cache/{cache_id}')
    data={
        'id':comment_id
    }
    Comment.delete_comment(data)
    return redirect (f'/view/cache/{cache_id}')

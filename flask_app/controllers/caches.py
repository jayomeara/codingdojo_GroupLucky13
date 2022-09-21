from functools import cache
from flask_app import app
from flask import render_template, redirect, request, session, flash

# Import classes
from flask_app.models.cache import Cache

# Default login / Registration page
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/newcache')
def add_cache():
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template('addcache.html')

@app.route('/postcache', methods=["POST"])
def post_new_cache():
    data={
        'latitude': request.form['latitude'],
        'longitude': request.form['longitude'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Cache.save_cache(data)
    return redirect ('/dashboard')

@app.route('/usercaches')
def view_caches():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : session['user_id']
        }
        userCaches = Cache.get_all_caches_by_user(data)
        return render_template('my_caches.html', userCaches=userCaches)

@app.route('/usercaches/delete/<int:cache_id>')
def delete_cache(cache_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : cache_id
        }
        Cache.delete_cache(data)
        return redirect('/usercaches')

@app.route('/usercaches/edit/<int:cache_id>')
def edit_cache(cache_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : cache_id
        }
        cache = Cache.get_cache_by_id(data)
        return render_template('edit_cache.html', cache=cache)

@app.route('/usercaches/update', methods=['POST'])
def update_cache():
    if 'user_id' not in session:
        return redirect('/')
    else:
        Cache.update_cache(request.form)
        return redirect('/usercaches')

@app.route('/cachemapsearch')
def map_search():
    if 'user_id' not in session:
        return redirect('/')
    else:
        allCaches=Cache.get_all_caches
        return render_template('search_map.html', allCaches=allCaches)

@app.route('/searchall', methods=['GET', 'POST'])
def search_by_location():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'latitude': request.form['latitude'],
            'longitude': request.form['longitude'],
            'user_id': session['user_id']
        }
        return redirect('/cachemapsearch')

# BUG: traceback error if there is not a comment
@app.route('/view/cache/<int:cache_id>')
def view_cache_with_comments(cache_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : cache_id
        }
        cache = Cache.get_cache_by_id(data)
        userCaches = Cache.get_cache_by_id_with_comments(data)
        return render_template('cache_with_comments.html', userCaches=userCaches, cache=cache)

@app.route('/get_all_caches')
def get_all_caches():
    return Cache.get_all_caches_JSON()
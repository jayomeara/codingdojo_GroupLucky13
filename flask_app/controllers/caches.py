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

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

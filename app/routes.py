from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@main.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.index'))

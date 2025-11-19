from flask import render_template
from . import main
from ..models import User 

@main.route('/')
def index():
    users_list = User.query.order_by(User.username).all()
    return render_template('index.html', 
                           users=users_list)
from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Role, EmailLog
from ..email import send_email
from . import main
from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user_role = Role.query.filter_by(name='User').first()
            if user_role is None:
                user_role = Role(name='User')
                db.session.add(user_role)
            
            user = User(username=form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            
            session['known'] = False
            
            if current_app.config['FLASKY_ADMIN']:
                
                send_email(current_app.config['FLASKY_ADMIN'], 
                           'Novo Usuário Cadastrado',
                           'mail/new_user', 
                           user=user) 
        else:
            session['known'] = True
        
        session['name'] = form.name.data
        return redirect(url_for('.index'))
        
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'),
                           known=session.get('known', False))

@main.route('/emails')
def emails():

    email_list = EmailLog.query.order_by(EmailLog.timestamp.desc()).all()
    return render_template('emails.html', emails=email_list)
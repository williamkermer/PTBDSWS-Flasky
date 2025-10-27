from flask import render_template, session, redirect, url_for, current_app
from datetime import datetime
import requests 

from . import main
from .. import db    
from ..models import User, Role, EmailLog
from .forms import NameForm

def send_simple_message(to, subject, newUser):
    app = current_app._get_current_object()
    email_body = f"Nome: William Kermer Romualdo\nProntuário: PT3032191\nNovo usuário cadastrado: {newUser}"
    full_subject = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject
    
    resposta = requests.post(app.config['API_URL'],
                             auth=("api", app.config['API_KEY']),
                             data={"from": app.config['API_FROM'],
                                   "to": to,
                                   "subject": full_subject,
                                   "text": email_body})
    
    if resposta:
        log_entry = EmailLog(
            sender=app.config['API_FROM'], recipient=str(to),
            subject=full_subject, body=email_body, timestamp=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.commit()
    return resposta

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
                destinatarios = [current_app.config['FLASKY_ADMIN'], "flaskaulasweb@zohomail.com"]
                send_simple_message(destinatarios, 'Novo usuário', form.name.data)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index')) 
    
    users_list = User.query.order_by(User.username).all()
    
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), users=users_list)

@main.route('/emails')
def emails():
    email_list = EmailLog.query.order_by(EmailLog.timestamp.desc()).all()
    return render_template('emails.html', emails=email_list)
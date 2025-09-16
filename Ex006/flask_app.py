#Exercício 6

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_moment import Moment
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "chave forte"
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators = [DataRequired()])
    last_name = StringField("Informe o seu sobrenome:", validators = [DataRequired()])
    institution = StringField("Informe a sua Instituição e Ensino:", [DataRequired()])
    course = SelectField("Informe a sua Disciplina:", choices=["DSWA5", "DWBA4", "Gestão de Projetos"])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField(validators = [DataRequired()])
    password = PasswordField(validators = [DataRequired()])
    submit = SubmitField('Submit')

# Rota - Página Inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome.')
        session['name'] = form.name.data
        session['last_name'] = form.last_name.data
        session['institution'] = form.institution.data
        session['course'] = form.course.data
        return redirect(url_for('index'))
    remote_addr = request.remote_addr
    host = request.host
    print("Sessão atual: ", dict(session))
    return render_template('index.html', form=form, name=session.get('name'), last_name=session.get('last_name'), institution=session.get('institution'), course=session.get('course'), remote_addr=remote_addr, host=host, current_time=datetime.utcnow())

'''
# Rota - Identificação 
@app.route("/user/<nome>/<prontuario>/<instituicao>")
def user_profile(nome="William Kermer", prontuario="PT3032191", instituicao="IFSP"):
    return render_template('user.html', name=nome, prontuario=prontuario, instituicao=instituicao)

# Rota - Requisição 
@app.route("/contextorequisicao/<nome>")
def contexto_requisicao(nome):
    user_agent = request.headers.get("User-Agent", "desconhecido")
    remote_ip  = request.remote_addr or "desconhecido"
    host       = request.host
    return render_template('req.html', name=nome, user_agent=user_agent, remote_ip=remote_ip, host=host)

'''
# Rota - Página Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = form.username.data
        return redirect(url_for('login_response'))
    return render_template('login.html', form=form, current_time=datetime.utcnow())

# Rota - Página Resposta do Login
@app.route('/loginResponse')
def login_response():
    return render_template('login-response.html', username=session.get('username'), current_time=datetime.utcnow())

# Por conveniência fiz um manipulador para qualquer outra rota não encontrada
@app.errorhandler(404)
def page_not_found(e):
    """Manipulador de erro para páginas não encontradas (404)."""
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
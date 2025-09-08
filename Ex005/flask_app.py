from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave forte'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Rota - Página Inicial
@app.route("/", methods=['GET', 'POST'])
def home():
    """Renderiza a página inicial com a data e hora atuais."""
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('home')) 
    return render_template('index.html', form=form, name=session.get('name'))

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

# Por conveniência fiz um manipulador para qualquer outra rota não encontrada
@app.errorhandler(404)
def page_not_found(e):
    """Manipulador de erro para páginas não encontradas (404)."""
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
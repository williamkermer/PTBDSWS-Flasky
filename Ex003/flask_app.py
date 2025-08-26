#Exercicio 3

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Rota - Página Inicial
@app.route("/")
def home():
    """Renderiza a página inicial com a data e hora atuais."""
    return render_template('index.html', current_time=datetime.utcnow())

# Rota - Hello User
@app.route('/user/<username>')
def user_profile(username):
    """Renderiza uma página de perfil para um usuário específico."""
    return render_template('user.html', name=username)

# Rota específica para a página de erro
@app.route('/rotainexistente')
def not_found_route():
    """Uma rota definida que mostra a página de erro 404."""
    return render_template('404.html'), 404

# Por conveniência fiz um manipulador para qualquer outra rota não encontrada
@app.errorhandler(404)
def page_not_found(e):
    """Manipulador de erro para páginas não encontradas (404)."""
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)

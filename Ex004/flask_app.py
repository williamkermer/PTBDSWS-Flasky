#Exercicio 4

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

@app.route("/user/<nome>/<prontuario>/<instituicao>")
def user_profile(nome = "William Kermer", prontuario="PT3032191", instituicao="IFSP"):

    return render_template('user.html', name=nome, prontuario=prontuario, instituicao=instituicao)

@app.route("/contextorequisicao/<nome>")
def contexto_requisicao(nome = "William Kermer"):
    user_agent = request.headers.get("User-Agent", "desconhecido")
    remote_ip  = request.remote_addr or "desconhecido"
    host       = request.host

    return render_template('req.html',name=nome, user_agent=user_agent, remote_ip=remote_ip, host=host)
    

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

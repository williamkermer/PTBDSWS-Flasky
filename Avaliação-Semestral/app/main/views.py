# 1. Adicionei 'flash' nas importações
from flask import render_template, redirect, url_for, flash
from datetime import datetime
from . import main
from .forms import NameForm, ProfessorForm
from .. import db
from ..models import Role, User

@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/professores', methods=['GET', 'POST'])
def professores():
    form = ProfessorForm()
    if form.validate_on_submit():
        # Verifica se o Professor JÁ EXISTE
        professor_existente = User.query.filter_by(username=form.name.data).first()
        
        if professor_existente:
            # 2. Mensagem de Erro/Aviso
            flash('Professor já existe na base de dados!')
        else:
            # Lógica da Disciplina (Role)
            disciplina_nome = form.role.data
            role = Role.query.filter_by(name=disciplina_nome).first()
            
            if role is None:
                role = Role(name=disciplina_nome)
                db.session.add(role)
                db.session.commit()
            
            # Cria o novo Professor
            professor = User(username=form.name.data, role=role)
            db.session.add(professor)
            db.session.commit()
            
            # 3. Mensagem de Sucesso
            flash('Professor cadastrado com sucesso!')
        
        return redirect(url_for('.professores'))
    
    professores_list = User.query.order_by(User.username).all()
    
    return render_template('professores.html', 
                           form=form, 
                           professores=professores_list)
                           
@main.route('/indisponivel')
def unavailable():
    return render_template('unavailable.html', current_time=datetime.utcnow())
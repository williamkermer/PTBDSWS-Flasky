from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired, Email


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    notification_email = StringField(
        'Qual é o seu email (Envio de notificação do novo usuário)?',
        validators=[DataRequired(message="Este campo é obrigatório."), 
                    Email(message="Formato de e-mail inválido.")]
    )

    submit = SubmitField('Submit')
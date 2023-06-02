from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeintergard.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        check_email = Usuario.query.filter_by(email=email.data).first()
        if check_email:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail.')
    
    def validate_username(self, username):
        check_username = Usuario.query.filter_by(username=username.data).first()
        if check_username:
            raise ValidationError('Usuário já cadastrado. Cadastra-se com outro usuário.')
        
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    lembrar_dados = BooleanField('Lembrar')
    botao_submit_login = SubmitField('Fazer Login')
    
    
class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_python = BooleanField('Curso de Python')
    curso_html = BooleanField('Curso de HTML')
    curso_css = BooleanField('Curso de CSS')
    curso_javascript = BooleanField('Curso de JavaScript')
    curso_react = BooleanField('Curso de React')
    curso_sql = BooleanField('Curso de SQL')
    botao_submit_editarperfil = SubmitField('Confirmar Alterações')
  
    def validate_email(self, email):
        if current_user.email != email.data:
            check_email = Usuario.query.filter_by(email=email.data).first()
            if check_email:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre-se com outro e-mail.')
            
    def validate_username(self, username):
        if current_user.username != username.data:
            check_username = Usuario.query.filter_by(username=username.data).first()
            if check_username:
                    raise ValidationError('Já exitse um usuário com esse nome. Cadastre-se com outro nome.')
                
                
class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')
    
class FormEditarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')
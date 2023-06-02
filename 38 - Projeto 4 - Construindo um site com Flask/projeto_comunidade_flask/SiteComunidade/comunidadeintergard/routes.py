from flask import render_template, url_for, request, flash, redirect, abort
from comunidadeintergard.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost, FormEditarPost
from comunidadeintergard.models import Post, Usuario
from comunidadeintergard import app, database, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuario = Usuario.query.all()
    return render_template('usuarios.html', lista_usuario=lista_usuario)

@app.route("/login&contato", methods=["GET", "POST"])
def login():
    form_login = FormLogin()  # Instância do formulário FormLogin
    form_criarconta = FormCriarConta()  # Instância do formulário FormCriarConta
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('contato'))
        else: 
            flash('Falha no login, E-mail ou Senha incorretos', 'alert-danger')
    
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
         senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
         usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
         database.session.add(usuario)
         database.session.commit()
        
         flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
         return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))
    
@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=["GET", "POST"])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(6)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (600, 600)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_curso(form):
    lista_cursos = []
    for campo in form:
        if 'curso' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';' .join(lista_cursos)


@app.route('/editar/perfil', methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_curso(form)
            
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(str(current_user.foto_perfil)))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<int:post_id>', methods=["GET", "POST"])
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        form = FormEditarPost()
        #Lógica para editar o post
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        #Lógica para editar o posto
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('exibir_post', post_id=post.id))
    else:
        form = None
        
    return render_template('post.html', post=post, form=form)


@app.route('/post/<int:post_id>/excluir', methods=["GET", "POST"])
@login_required
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
        
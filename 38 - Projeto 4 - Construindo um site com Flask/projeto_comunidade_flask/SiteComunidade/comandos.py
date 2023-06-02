# from comunidadeintergard import database
# from comunidadeintergard import app
# from comunidadeintergard.models import Usuario, Post

# with app.app_context():
#      database.create_all()

# with app.app_context():
#     usuario_thiarly = Usuario(username='thiarly', email='thiarly.cavalcante@live.com', senha='123456')
# #     usuario_luca = Usuario(username='luca', email='luca.cavalcante@live.com', senha='123456')
#     database.session.add(usuario_thiarly)
# #     database.session.add(usuario_luca)
#     database.session.commit()

# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     print(meus_usuarios)
#     print(meus_usuarios[0].username)
#     print(meus_usuarios[0].email)
#     print(meus_usuarios[0].senha)
#     print(meus_usuarios[0].posts)


# with app.app_context():
#     usuario_pesquisa = Usuario.query.filter_by(id=2).first()
#     print(usuario_pesquisa.email)

# with app.app_context():
#     usuario_pesquisa = Usuario.query.filter_by(email='thiarly.cavalcante@live.com').first()
#     print(usuario_pesquisa.username)


# with app.app_context():
#     meu_post = Post(id_usuario=1, titulo='Primeiro Post', corpo='Luca Voando')
#     database.session.add(meu_post)
#     database.session.commit()


# with app.app_context():
#     post = Post.query.first()
#     print(post.titulo)
#     print(post.autor.email)


# with app.app_context():
#     database.drop_all()
#     database.create_all()

from comunidadeintergard import app, database

with app.app_context():
    database.create_all()

if __name__ == '__main__':
    app.run(debug=True)

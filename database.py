import hashlib

# ORM peewee for MySQL u other databases *
from peewee import *
from datetime import datetime

database = MySQLDatabase('fastapi_project', 
                         user='root',
                         password='root',
                         host='localhost',
                         port=3306)

# Diseño de Modelos para las Tablas siempre heredan de Model
# Atributos = columnas en tablas
class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)
    
    # Info a imprimir cuando se agrague un usuario
    def __str__(self):
        return self.username
    
    # Asignamos la base de datos y la tabla
    class Meta:
        database = database
        table_name = 'users'
    
    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()
        
class Movie(Model):
    title = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title
    
    class Meta:
        database = database
        table_name = 'movies'
        
class UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews')
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'
    
    class Meta:
        database = database
        table_name = 'user_reviews'
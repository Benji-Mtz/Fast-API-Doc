# Los Schemas nos serviran para validar datos de entrenda y salida de cada modelo de clase

# Tipo de dato any 
from typing import Any
# decorador validator para validar los datos de entrada
from pydantic import validator

# Verifica que los datos de las clases correspondan con los datos de la base de datos
from pydantic import BaseModel

# GetterDict convertida en JSON y ModelSelect hara match de UserResponseModel con alguna Clase de database.py
from pydantic.utils import GetterDict
from peewee import ModelSelect

# Esta clase serializarara el modelo de la base de datos a un JSON solo con el ORM Pewee
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res

# Esta clase convertira modelos de ORM Pewee a Pydantic (valores de entrada y / o salida)
class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

# ------------ User ------------
class UserRequestModel(BaseModel):
    username: str
    password: str
    
    # Validamos que el username este entre 3 - 50 caracteres
    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud debe encontrarse entre 3 y 50 caracteres.')
        
        return username
    # TODO: Validar que la contraseña no este vacia

class UserResponseModel(ResponseModel):
    id: int
    username: str    
    
# ------------ Review ------------
class ReviewValidator():
    
    @validator('score')
    def score_validator(cls, score):
        
        if score < 1 or score > 5:
            raise ValueError('El rango para score es de 1 a 5.')
        return score
        
class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movie_id: int
    review: str
    score: int
        
    
class ReviewResponseModel(ResponseModel):
    id: int
    movie_id: int
    review: str
    score: int
    
class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int
    
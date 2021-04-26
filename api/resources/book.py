from flask import request
from flask_restful import Resource
from resources.utils import tupleStatus
from model.db import Books, Clients

import time
import datetime

# Classes que buscam e alteram informações de livros no banco e passam esse resultado na resposta da API

class Book(Resource):
    def put(self, id):
        book = Books.query.filter_by(id=id).first()
        try:
            data = request.json
            if book.status == tupleStatus.index("Emprestado"):
                response = {
                    'status':'Erro',
                    'message':'O livro já se encontra emprestado'
                }
            elif not Clients.query.filter_by(id=data['client_id']).first():
                response = {
                    'status':'Erro',
                    'message':'O cliente não foi encontrado'    
                }
            else :
                client_id = data['client_id']
                book.status = tupleStatus.index("Emprestado")
                book.client_id = client_id
                book.reserveTime = time.time()
                book.save()
                timestamp = datetime.datetime.fromtimestamp(book.reserveTime)
                response = {
                    'status':'Sucesso',
                    'message':'Livro reservado com sucesso',
                    'details':{
                        'name':book.name,
                        'reserved_date' : timestamp.strftime('%Y-%m-%d')
                    }
                }
        except AttributeError:
            response = {
                'status':'Erro',
                'message':'O livro não foi encontrado'
            }
        return response

class BookList(Resource):
    def get(self):
        books = Books.query.all()
        response = [{'id':i.id,'name':i.name, 'status':tupleStatus[i.status]} for i in books]
        return response
    
    def post(self):
        data = request.json
        if Books.query.filter_by(name=data['name']).first():
            response = {
                'status':'Erro',
                'message':'Livro já cadastrado'
            }
        else:
            book = Books(name=data['name'], author=data['author'],status=tupleStatus.index("Disponível"),client_id=0, reserveTime=0)
            book.save()
            timestamp = datetime.datetime.fromtimestamp(book.reserveTime)
            response = {
                'status':'Sucesso',
                'message':'Livro inserido com sucesso',
                'details':{
                    'id':book.id,
                    'name':book.name,
                    'author':book.author,
                    }
            }
        return response
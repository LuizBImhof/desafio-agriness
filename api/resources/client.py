from flask import request
from flask_restful import Resource
from resources.utils import tupleStatus
from model.db import Clients, Books
from resources.utils import VALUE_RESERVE
import time
import datetime

# Classes que buscam e alteram informações de clientes no banco e passam esse resultado na resposta da API

class Client(Resource):
    def get(self):
        clients = Clients.query.all()
        response = [{'id':i.id,'name':i.name} for i in clients]
        return response
        
    def post(self):
        data = request.json
        if Clients.query.filter_by(name=data['name']).first():
            response = {
                'status':'Erro',
                'message':'Cliente já cadastrado'
            }
        else:
            client = Clients(name=data['name'])
            client.save()
            response = {
                'status':'Sucesso',
                'message':'Cliente inserido com sucesso',
                'details':{
                    'id':client.id,
                    'name':client.name
                }
            }
        return response

# Classe usada para buscar os livros emprestados atualmente para o cliente e para calcular o valor devido

class ClientReserves(Resource):
    def get(self, id_client):
        if Clients.query.filter_by(id=id_client).first():
            books = Books.query.filter_by(status=tupleStatus.index("Emprestado"), client_id=id_client)
            response =[{'name':i.name, 
                        'dateReserve':datetime.datetime.fromtimestamp(i.reserveTime).strftime('%Y-%m-%d'), 
                        'days':self.getDaysReserved(i),
                        'fee': self.getLateFee(self.getDaysReserved(i))
                        } for i in books]
        else:
            response = {
                'status':'Erro',
                'message':'O cliente não foi encontrado'
            }
        return response

    # Usa o timestamp da data que foi reservado e o timestamp atual para calcular quantos dias o livro está com o cliente 
    def getDaysReserved(self,book):
        reservedDate = datetime.datetime.fromtimestamp(book.reserveTime)
        now = datetime.datetime.fromtimestamp(time.time())
        return int((now-reservedDate).days)

    # Calcula a taxa de acordo com as regras de juros, multas e o valor da reserva de um livro
    def getLateFee(self,days):
        if 3 < days and days < 6 :
            return VALUE_RESERVE + (VALUE_RESERVE*0.3) + (VALUE_RESERVE*(days-3)*0.02)
        elif 6 <= days and days < 8:
            return VALUE_RESERVE + (VALUE_RESERVE*0.5) + (VALUE_RESERVE*(days-3)*0.04)
        elif 8 <= days:
            return VALUE_RESERVE + (VALUE_RESERVE*0.7) + (VALUE_RESERVE*(days-3)*0.06)
        else:
            return VALUE_RESERVE
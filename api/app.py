from flask import Flask, request
from flask_restful import Resource, Api
from resources.book import Book, BookList
from resources.client import Client, ClientReserves

app = Flask(__name__)
api = Api(app)

# Rotas que estão disponíveis na API 

api.add_resource(ClientReserves, '/client/<int:id_client>/books')
api.add_resource(Book, '/books/<int:id>/reserve')
api.add_resource(BookList, '/books')
api.add_resource(Client, '/clients')

if __name__ == '__main__':
    app.run(debug=True)
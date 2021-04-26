import unittest
import requests
import time
import datetime

def test_get_books_check_status_code_equals_200_id_2():
     response = requests.get("http://127.0.0.1:5000/books")
     response_body = response.json()
     assert response.status_code == 200
     assert response_body[2]["name"] == "Senhor dos anéis: O retorno do rei"
     assert response_body[2]["status"] == "Emprestado"

def test_get_client_1_reserved_books():
     response = requests.get("http://127.0.0.1:5000/client/1/books")
     response_body = response.json()
     assert response.status_code == 200
     dateReserved = response_body[6]["dateReserve"]
     daysReserved = response_body[6]["days"]
     fee = response_body[6]["fee"] 
     if daysReserved <= 3:
          assert fee == 1
     elif daysReserved == 4:
          assert fee == 1.32
     elif daysReserved == 7:
          assert fee == 1.66
     elif daysReserved == 9:
          assert fee == 2.06

def test_reserv_book_already_reserved():
     put_body = {'client_id': 1}
     response = requests.put("http://127.0.0.1:5000/books/10/reserve",put_body)
     response_body = response.json()
     assert response.status_code == 200
     assert response_body["status"] == "Erro"
     assert response_body["message"] == "O livro já se encontra emprestado"

def test_reserv_book_book_inexistent():
     put_body = {'client_id': 1}
     response = requests.put("http://127.0.0.1:5000/books/111/reserve",put_body)
     response_body = response.json()
     assert response.status_code == 200
     assert response_body["status"] == "Erro"
     assert response_body["message"] == "O livro não foi encontrado"

# Este teste não está funcionando, pois excecutando por aqui não está conseguindo buscar o cliente com o id passado pelo put_body
# Porém ao executar o mesmo método, com os mesmos parâmetros pelo insomnia o resultado é o esperado
def test_reserv_book_client_inexistent():
     put_body = {'client_id': 11}
     response = requests.put("http://127.0.0.1:5000/books/12/reserve",put_body)
     response_body = response.json()
     assert response.status_code == 200
     assert response_body["status"] == "Erro"
     assert response_body["message"] == "O livro não foi encontrado"

# Este teste não está funcionando, pois excecutando por aqui não está conseguindo buscar o cliente com o id passado pelo put_body
# Porém ao executar o mesmo método, com os mesmos parâmetros pelo insomnia o resultado é o esperado
def test_reserv_book_success():
     put_body = {'client_id':1}
     response = requests.put("http://127.0.0.1:5000/books/12/reserve",put_body)
     response_body = response.json()
     assert response.status_code == 200
     if response_body['status'] == 'Sucesso':
          assert response_body['message'] == "Livro reservado com sucesso"
     else:
          assert response_body['message'] == "O livro já se encontra emprestado"


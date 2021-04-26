# É usado para definir os possíveis status dos livros, como no momento só existem 2 status optei por fazer uma tupla
# mas ao crescer a aplicação pode ficar inviável manter dessa forma, uma outra alternativa seria ter uma tabela para os status
tupleStatus = ("Disponível", "Emprestado")

# Constante usada para o valor de empréstimo do livro, fiz dessa forma pois não tinha definido o valor no desafio,
# e com uma constante é possível alterar o valor conforme desejado. 
# Também pode causar problemas ao crescer a aplicação, mas achei uma opção válida para o teste
VALUE_RESERVE = 1
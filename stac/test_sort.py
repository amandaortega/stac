from sort_algorithms import sort_algorithms

database_path = '/home/amanda/Dropbox/trabalho/doutorado/testes/vento/Brasil/resultados/RMSE/resultados.csv'
alpha = 0.05
[rankings, better, worse] = sort_algorithms(database_path, alpha)

print(rankings, '\n')
print(better, '\n')
print(worse)
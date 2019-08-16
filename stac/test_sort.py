from sort_algorithms import sort_algorithms

def print_sort(database_path, alpha, header):
    print(header)

    [rankings, average, better, worse] = sort_algorithms(database_path, alpha)

    print('Rankings: ', rankings, '\n')
    print('Average: ', average, '\n')
    print('#<: ', worse, '\n')
    print('#>: ', better, '\n')
    print()

print_sort('/home/amanda/Dropbox/trabalho/doutorado/testes/aplicacoes/vento/USA/resultados/geral/2/RMSE_complete.csv', 0.05, 'RMSE complete')
#print_sort('/home/amanda/Dropbox/trabalho/doutorado/testes/aplicacoes/vento/USA/resultados/geral/2/RMSE_test.csv', 0.05, 'RMSE test')
print_sort('/home/amanda/Dropbox/trabalho/doutorado/testes/aplicacoes/vento/USA/resultados/geral/2/rules_mean.csv', 0.05, 'Rules')
print_sort('/home/amanda/Dropbox/trabalho/doutorado/testes/aplicacoes/vento/USA/resultados/geral/2/time.csv', 0.05, 'Time')
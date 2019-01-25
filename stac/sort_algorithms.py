from nonparametric_tests import friedman_test, finner_multitest
import csv
import numpy as np
from collections import OrderedDict

def sort_algorithms(database_path, alpha):
    database = []

    with open(database_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            database.append(row)

    database = np.asarray(database)

    [F_value, p_value, rankings, pivots] = friedman_test(database[1:, 1], database[1:, 2], database[1:, 3], database[1:, 4], database[1:, 5], database[1:, 6], database[1:, 7], database[1:, 8], database[1:, 9], database[1:, 10], database[1:, 11], database[1:, 12])

    dic_rankings = {}
    dic_pivots = {}
    dic_better = {}
    dic_worse = {}

    for i in range (1, database.shape[1]):
        dic_rankings[database[0, i]] = rankings[i-1]
        dic_pivots[database[0, i]] = pivots[i-1]
        dic_better[database[0, i]] = 0
        dic_worse[database[0, i]] = 0        

    [comparions, Z_values, p_values, adjusted_p_values] = finner_multitest(dic_pivots)

    for i in range(len(comparions)):
        [alg1, alg2] = comparions[i].split(' vs ')
        
        # H0 is rejected
        if adjusted_p_values[i] <= alpha:
            if dic_rankings[alg1] < dic_rankings[alg2]:
                dic_better[alg1] = dic_better[alg1] + 1
                dic_worse[alg2] = dic_worse[alg2] + 1
            else:
                dic_better[alg2] = dic_better[alg2] + 1
                dic_worse[alg1] = dic_worse[alg1] + 1  

    better = sorted(dic_better.items(), key=lambda kv: dic_rankings[kv[0]])
    worse = sorted(dic_worse.items(), key=lambda kv: dic_rankings[kv[0]])
    rankings = sorted(dic_rankings.items(), key=lambda kv: dic_rankings[kv[0]])

    return [rankings, better, worse]             
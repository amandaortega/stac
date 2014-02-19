# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:33:54 2014

@author: Adrián
"""

import scipy as sp
import scipy.stats as st

#Para cuando el tamaño muestral N sea menor o igual a 25, se puede hacer el test de Wilcoxon
#examinando la tabla que nos da los valores críticos (el intervalo) para cada valor de N y
#nivel de significancia (0.10,0.05,0.02,0.01,0.005,0.001) dado. Si tenemos en cuenta que T
#será el valor mínimo de (suma rangos positivos, suma rangos negativos), se utilizan los límites
#inferiores de los intervalos y el contraste será estadísticamente significativo si: T <= límite
#inferior correspondiente.
tabla_wilcoxon = {0.10:{5:0,6:2,7:3,8:5,9:8,10:10,11:13,12:17,13:21,14:25,15:30,16:35,17:41,
                    18:47,19:53,20:60,21:67,22:75,23:83,24:91,25:100},
                  0.05:{6:0,7:2,8:3,9:5,10:8,11:10,12:13,13:17,14:21,15:25,16:29,17:34,18:40,
                    19:46,20:52,21:58,22:65,23:73,24:81,25:89},
                  0.02:{7:0,8:1,9:3,10:5,11:7,12:9,13:12,14:15,15:19,16:23,17:27,18:32,19:37,
                    20:43,21:49,22:55,23:62,24:69,25:76},
                  0.01:{8:0,9:1,10:3,11:5,12:7,13:9,14:12,15:15,16:19,17:23,18:27,19:32,20:37,
                    21:42,22:48,23:54,24:61,25:68},
                  0.005:{9:0,10:1,11:3,12:5,13:7,14:9,15:12,16:15,17:19,18:23,19:27,20:32,
                    21:37,22:42,23:48,24:54,25:60},
                  0.001:{11:0,12:1,13:2,14:4,15:6,16:8,17:11,18:14,19:18,20:21,21:25,22:30,
                    23:35,24:40,25:45}}

def wilcoxon_test(matriz_datos, alpha, tipo):

    #El test de Wilcoxon compara dos algoritmos.
    if len(matriz_datos[0]) != 2:
        return {"fallo" : "Test de Wilcoxon solo aplicable a dos algoritmos"}
    
    #Paso de una matriz de conjuntos de datos a dos listas: lista "a", que contiene
    #los resultados de aplicar el primer algoritmo a los datos y una lista "b" que
    #contiene los resultados de aplicar el segundo algoritmo sobre los mismos datos.
    a = []
    b = []
    for lista_datos in matriz_datos:
        a.append(lista_datos[0])
        b.append(lista_datos[1])
    
    #Cálculo del número de veces que se aplican los dos algoritmos, es decir,
    #el número de individuos o datos sobre los que se aplican los algoritmos. El
    #tamaño de a y b deben ser iguales. Se conoce como tamaño muestral. Hay
    #dos muestras: a y b.
    N = len(a)
    
    #Cálculo de las diferencias sin signos y con signos. Se excluye el 0.
    diferencias = []
    signos = []
    for i in range(N):
        diferencia = a[i]-b[i]
        if diferencia != 0:
            diferencias.append(abs(diferencia))
            signos.append(diferencia)
    
    #Tamaño muestral después de eliminar las diferencias 0.
    N = len(diferencias)

    #El tamaño de la muestra  (sin ligaduras) debe ser al menos de 5.
    if N < 5:
        return {"fallo" : "Menos de 5 conjuntos de datos sin ligaduras"}

    #Rangos de orden 1,2,...,N. Cada elemento de copia tiene un rango asociado:
    #indice(elemento) + 1. Si hay empates se calcula la media del rango de cada
    #uno de los elementos repetidos.
    copia = list(diferencias)
    copia.sort()
    rangos = []
    for i in diferencias:
        rangos.append((copia.count(i)+copia.index(i)*2+1)/float(2))
    
    #Sumas de los rangos de las Di mayores que 0 y menores que 0.
    mayor0 = []
    menor0 = []
    for i in range(N):
        if signos[i] > 0:
            mayor0.append(rangos[i])
        else:
            menor0.append(rangos[i])
    T_Mas = sp.sum(mayor0)
    T_Men = sp.sum(menor0)

    #T es el valor mínimo de T_Mas y T_Men.
    T = min(T_Mas,T_Men)
    
    print "N (sin ceros):" , N
    print "Suma de rangos positivos:" , T_Mas
    print "Suma de rangos negativos:" , T_Men
    print "Valor T:" , T
    
    #Para tamaños muestrales pequeños, se puede determinar el test de Wilcoxon mediante la comparación
    #de T con el valor crítico de la tabla de Wilcoxon. Para tamaños muestrales grandes, el test se puede
    #aproximar con la distribución normal.
    if N <= 25:
        #Límite inferior del intervalo de aceptación.
        punto_critico = tabla_wilcoxon[alpha][N]
        return {"resultado" : str(T <= punto_critico), "estadistico" : T, "suma rangos pos" : T_Mas, "suma rangos neg" : T_Men ,
        "punto critico" : punto_critico}
    else:
        #Cálculo del valor Z
        Z = (T-((N*(N+1))/4))/sp.sqrt((N*(N+1)*(2*N+1))/24)
        #Cálculo del punto critico de la distribución Normal (Para alpha = 0.05
        #es -1.96 en el caso de dos colas, es decir 0.025 a cada lado).
        Z_alphaDiv2 = st.norm.ppf(alpha/2)
        #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo
        #como el estadístico Z.
        p_valor = 2*(1-st.norm.cdf(abs(Z)))
        
        print "Valor Z:" , Z
        print "Valor Z_alphaDiv2:" , Z_alphaDiv2
        print "p_valor:" , p_valor
        
        #Si p_valor < alpha => contraste estadísticamente significativo. Otra 
        #forma de saber si el estadístico Z cae en la región de rechazo es:
        #if Z <= Z_alphaDiv2 or Z >= -Z_alphaDiv2:
            #print "Se rechaza H0."
        #else:
            #print "Se acepta HO."
        
        return {"resultado" : str(p_valor < alpha), "p_valor" : round(p_valor,5), "estadistico" : round(Z,5),
        "suma rangos pos" : T_Mas, "suma rangos neg" : T_Men, "puntos criticos" : [round(Z_alphaDiv2,2),round(-Z_alphaDiv2,2)]}
        
def friedman_test(nombres_algoritmos, matriz_datos, alpha, tipo):
    
    #Número de algoritmos.
    K = len(nombres_algoritmos)
    
    #El test de Friedman compara al menos dos algoritmos.
    if K < 2:
        return {"fallo" : "Test de Friedman necesita al menos 2 algoritmos"}

    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)
    
    #Asignación de rankings a los resultados obtenidos por cada algoritmo en cada problema.
    #Cada fila representa un conjunto de datos compuesto por los valores (rankings) asignados.
    #Los valores se asignan de forma ascencente: 1 al mejor resultado, 2 al segundo, etc. En
    #caso de empates, se asignan valores medios.
    rankings = []
    for conj_datos in matriz_datos:
        ranking_conj = []
        copia = list(conj_datos)
        #Ordenamos según el problema se tratase de maximizar o minimizar.
        copia.sort(reverse=tipo)
        for dato in conj_datos:
            ranking_conj.append((copia.count(dato)+copia.index(dato)*2+1)/float(2))
        rankings.append(ranking_conj)
    
    #Cálculo de los rankings medios de los algoritmos sobre los N problemas.
    rankings_medios = []
    for i in range(K):
        rankings_medios.append(sp.mean([fila[i] for fila in rankings]))

    #Cálculo del estadístico de Friedman, que se distribuye como una distribución chi-cuadrado
    #con K-1 grados de libertad, siendo K el número de variables relacionadas (o número de algoritmos).
    chi2 = ((12*N)/(K*(K+1)))*((sp.sum(r**2 for r in rankings_medios))-((K*(K+1)**2)/4))
    
    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico 
    #chi2.
    p_valor = 1 - st.chi2.cdf(chi2, K-1)
    
    #Cálculo del ranking final (tanto nombres de algoritmos como rankings medios) ordenado por el tipo de
    #problema (minimización o maximización). datos_ordenados es una lista de tuplas (cada tupla representa
    #el nombre del algoritmo y el valor) que están ordenadas por el valor de cada tupla.
    datos_ordenados = sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), 
                              key = lambda t:t[1], reverse=tipo)
    ranking_nombres = []
    ranking_valores = []
    for i in datos_ordenados:
        ranking_nombres.append(i[0])
        ranking_valores.append(i[1])
    
    return {"resultado" : str(p_valor < alpha), "p_valor": round(p_valor,5), "estadistico" : round(chi2,5), 
    "nombres" : ranking_nombres, "ranking" : ranking_valores}
    
def iman_davenport_test(nombres_algoritmos, matriz_datos, alpha, tipo):

    #Número de algoritmos.
    K = len(nombres_algoritmos)
    
    #El test de Iman-Davenport compara al menos dos algoritmos.
    if K < 2:
        return {"fallo" : "Test de Iman-Davenport necesita al menos 2 algoritmos"}
    
    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)
    
    # Cálculo del estadistico de Friedman.
    friedman = friedman_test(nombres_algoritmos, matriz_datos, alpha, tipo)
    chi2 = friedman["estadistico"]

    # Cálculo del estadistico de Iman-Davenport, que se distribuye de acuerdo a una distribución
    #f con (K-1) y (K-1)(N-1) grados de libertad.
    iman_davenport = ((N-1)*chi2)/(N*(K-1)-chi2)
    
    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico 
    #iman_davenport.
    p_valor = 1 - st.f.cdf(iman_davenport, K-1, (K-1)*(N-1))

    return {"resultado" : str(p_valor < alpha), "p_valor": round(p_valor,5), "estadistico" : round(iman_davenport,5), 
    "nombres": friedman["nombres"], "ranking": friedman["ranking"]}


"""
nombres_algoritmos = ["PSO","SSGA","SS_BLX","DE_EXP"]
matriz_datos = [[1.23E-01,8.42E-06,3.40E+02,8.26E-06],
        [2.60E+01,8.72E-02,1.73E+03,8.18E-06],
        [5.17E+07,7.95E+07,1.84E+08,9.94E+04],
        [2.49E+03,2.59E+00,6.23E+03,8.35E-06],
        [4.10E+05,1.34E+05,2.19E+03,8.51E-06],
        [7.31E+05,6.17E+03,1.15E+05,8.39E-06],
        [2.68E+02,1.27E+06,1.97E+06,1.27E+06],
        [2.04E+04,2.04E+04,2.04E+04,2.04E+04],
        [1.44E+04,7.29E-06,4.20E+03,8.15E-06],
        [1.40E+04,1.71E+04,1.24E+04,1.12E+04],
        [5.59E+03,3.26E+03,2.93E+03,2.07E+03],
        [6.36E+05,2.79E+05,1.51E+05,6.31E+04],
        [1.50E+03,6.71E+02,3.25E+02,6.40E+02],
        [3.30E+03,2.26E+03,2.80E+03,3.16E+03],
        [3.40E+05,2.92E+05,1.14E+05,2.94E+05],
        [1.33E+05,1.05E+05,1.04E+05,1.13E+05],
        [1.50E+05,1.19E+05,1.18E+05,1.31E+05],
        [8.51E+05,8.06E+05,7.67E+05,4.48E+05],
        [8.50E+05,8.90E+05,7.56E+05,4.34E+05],
        [8.51E+05,8.89E+05,7.46E+05,4.19E+05],
        [9.14E+05,8.52E+05,4.85E+05,5.42E+05],
        [8.07E+05,7.52E+05,6.83E+05,7.72E+05],
        [1.03E+06,1.00E+06,5.74E+05,5.82E+05],
        [4.12E+05,2.36E+05,2.51E+05,2.02E+05],
        [5.10E+05,1.75E+06,1.79E+06,1.74E+06]]
"""
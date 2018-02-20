# -*- coding: utf-8 -*-

__auth = ''

'''Devuelve el nº de clases de los ejemplos del conjunto
que se pasa como parámetro de entrada. Ejemplo de salida
de la función: {'0':519, '1':264}. El parámetro de entrada
porcentaje indica si se quiere que la proporción de clases
se devuelva en proporción al total de ejemplos. Ejemplo de
salida con porcentaje=True: {'0':0.66,'1':0.33}.'''

def proporcionClase(conjunto, porcentaje=False):
    proporcion = dict()
    for x in conjunto:
        clase = x[len(x)-1]
        if clase not in proporcion.keys():
            proporcion[clase] = 1
        else:
            proporcion[clase] += 1
    if porcentaje:
        for x in proporcion:
            proporcion[x] = proporcion[x]/len(conjunto)
    return proporcion

'''La función ejemplosClase devuelve un subconjunto de
ejemplos en los que aparece el valor de clasificación
que se pasa como parámetro de entrada.'''

def ejemplosClase(conjunto, clase):
    ejemplosClase = []
    for x in conjunto:
        claseX = x[len(x)-1]
        if clase == claseX:
            ejemplosClase.append(x)
    return ejemplosClase

'''La función subconjuntosValorAtributo devuelve un nuevo
subconjunto del conjunto de entrada en el que esté presente
el valor de entrada para un atributo concreto (que se determina
a partir del índice)'''

def subconjuntoValorAtributo(conjunto, indice=0, valor=None):
    subconjunto = []
    for x in conjunto:
        if x[indice] == valor:
            subconjunto.append(x)
    return subconjunto
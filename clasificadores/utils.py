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
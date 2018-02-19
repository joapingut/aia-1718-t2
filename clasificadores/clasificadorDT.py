# -*- coding: utf-8 -*-
from clasificadores.clasificador import Clasificador, NodoDT, ClasificadorNoEntrenado
from clasificadores.utils import proporcionClase
import math

'''ClasificadorDT es subclase de Clasificador, a lo que se añade
un campo entrenado que indica si el entrenamiento se ha realizado,
en caso negativo, se devuelve una excepción ClasificadorNoEntrenado.'''

class ClasificadorDT(Clasificador):
    
    def __init__(self, clasificacion, clases, atributos):
        super().__init__(clasificacion, clases, atributos)
        self.entrenado = False
        
    def entrena(self, entrenamiento, medida="entropia", maxima_frecuencia=1, minimo_ejemplos=0):
        self.entrenamiento = entrenamiento
        self.medida = medida
        self.maxima_frecuencia = maxima_frecuencia
        self.minimo_ejemplos = minimo_ejemplos
        self.arbol = entrenador(self.entrenamiento,self.medida,self.maxima_frecuencia,self.minimo_ejemplos)
        self.entrenado = True
    
    def clasifica(self, ejemplo):
        if self.entrenado:
            return clasificador(ejemplo,self.arbol)
        else:
            return ClasificadorNoEntrenado(Exception)
    
    def evalua(self, prueba):
        if self.entrenado:
            return evaluador(prueba,self.arbol)
        else:
            return ClasificadorNoEntrenado(Exception)
    
    def imprime(self):
        if self.entrenado:
            return imprimir(self.arbol)
        else:
            return ClasificadorNoEntrenado(Exception)

'''La función medidas realiza la función que se utilizará
para cuantificar el grado de clasificación dependiendo de la
medida que entre como entrada.'''

def medidas(medida, conjunto):
    result = 0.0
    proporcionClases = proporcionClase(conjunto)
    
    if medida=="entropia":
        for p in proporcionClases:
            result = result + proporcionClases[p]*math.log2(proporcionClases[p])
        result = -result
        
    elif medida=="error":
        result = 1 - proporcionClases[max(proporcionClases, key=proporcionClases.get)] / len(conjunto)
    
    elif medida=="gini":
        for p in proporcionClases:
            result = result + proporcionClases[p]*proporcionClases[p]
        result = 1 - result
    
    return result

'''Devuelve el nº de ejemplos del conjunto de entrada por valor
del atributo para conocer la proporción de ejemplos respecto al
total dependiendo del índice (que determina el atributo). Ejemplo
de salida: {'1st': 193, '2nd': 168, '3rd': 422}. Al igual que
en proporcionClase, si porcentaje=True, se devuelven los valores
respecto al número total de ejemplos.'''

def proporcionEjemplo(conjunto, indice=0, porcentaje=False):
    proporcion = dict()
    for x in conjunto:
        valor = x[indice]
        if valor not in proporcion.keys():
            proporcion[valor] = 1
        else:
            proporcion[valor] += 1
    if porcentaje:
        for x in proporcion:
            proporcion[x] = proporcion[x]/len(conjunto)
    return proporcion

'''indiceAtributo devuelve una lista con todos los atributos
ordenados por el mismo orden que en los atributos con sus posibles
valores, de manera que, para una entrada tal que: 
[('clase',['1st','2nd','3rd']),('edad',['niño','adulto']),('genero',['male','female'])],
el resultado sería ['clase', 'edad', 'genero'].'''

def indiceAtributo(atributos):
    indices = []
    for atributo in atributos:
        indices.append(atributo[0])
    return indices

'''La función clasificador recibe un ejemplo como parámetro de entrada
con valores por cada atributo y, a partir del árbol generado en el
entrenamiento, se devuelve un valor de clasificación final. Se recorre
el árbol por cada valor de atributo del ejemplo hasta llegar al nodo
hoja de dicho camino y se devuelve como resultado'''

def clasificador(ejemplo,arbol):
    if arbol.ramas != None:
        for valor in arbol.ramas:
            if ejemplo[arbol.atributo] == valor:
                clasificacion = clasificador(ejemplo,arbol.ramas[valor])
    else:
        clasificacion = arbol.clase
    return clasificacion

'''La función evaluador comprueba mediante un conjunto de validación
el rendimiento del árbol obtenido en el entrenamiento. Para cada ejemplo
del conjunto de validación, crea una copia, elimina el último elemento
(que es el valor de clasificación) y aprovecha la función clasificador
para que devuelva el valor de clasificación que tendría según el árbol.
Una vez hecho esto, comprueba si dicho valor es igual al que tiene
en dicho ejemplo, en caso afirmativo, suma 1 al número de aciertos. Una 
vez finalizado el bucle, se devuelve el número de aciertos dividido entre
 el número total de ejemplos del conjunto de validación.'''

def evaluador(prueba,arbol):
    aciertos = 0
    for ejemplo in prueba:
        copiaEjemplo = ejemplo
        copiaEjemplo.pop()
        if clasificador(copiaEjemplo,arbol) == ejemplo[len(ejemplo)-1]:
            aciertos += 1
    return aciertos/len(prueba)

'''La función imprimir devuelve una representación del árbol que
se pasa como parámetro de entrada a partir de los distintos subárboles
de sus ramas y la profundidad en el árbol. Se representa el valor de 
cada nivel de profundidad y el valor del atributo por cada rama, además
de una indentación que depende de la profundidad para una representación
más clara de las ramas. Si el nodo que se trata no tiene ramas, es un nodo
hoja y se representa el valor de clasificación.'''

def imprimir(arbol,profundidad=0):
    resultado = ""
    if arbol.ramas != None:
        for rama in arbol.ramas:
            resultado += "\t"*profundidad+str(profundidad)+": "+rama+"\n"+imprimir(arbol.ramas[rama],profundidad+1)
    else:
        resultado = "\t"*profundidad+str(profundidad)+": "+arbol.clase+"\n"
    return resultado



def entrenador(conjunto, medida="entropia", maxFrecuencia=1, minEjemplos=0):
    
    
    proporcionClases = proporcionClase(conjunto,True)
    proporcionEjemplos = proporcionEjemplo(conjunto,True)
    #if(max(proporcionClase(conjunto,True))
    
    
    
# -*- coding: utf-8 -*-
import copy
from clasificadores.clasificadorDT import clasificador, evaluador, imprimir, entrenador
from clasificadores.clasificador import Clasificador, NodoDT, ClasificadorNoEntrenado

'''ClasificadorDTPoda es subclase de Clasificador, a lo que se añade
un campo entrenado que indica si el entrenamiento se ha realizado,
en caso negativo, se devuelve una excepción ClasificadorNoEntrenado.
Además, se ha añadido en entrena un nuevo parámetro validacion para
la post-poda del árbol'''

class ClasificadorDTPoda(Clasificador):
    
    def __init__(self, clasificacion, clases, atributos):
        super().__init__(clasificacion, clases, atributos)
        self.entrenado = False
        
    def entrena(self, entrenamiento, medida="entropia", maxima_frecuencia=1, minimo_ejemplos=0, validacion=None):
        self.entrenamiento = entrenamiento
        self.medida = medida
        self.maxima_frecuencia = maxima_frecuencia
        self.minimo_ejemplos = minimo_ejemplos
        self.validacion = validacion
        self.arbol = entrenadorPoda(self.entrenamiento,self.medida,self.maxima_frecuencia,self.minimo_ejemplos,self.validacion)
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
        
def entrenadorPoda(conjunto, medida="entropia", maxFrecuencia=1, minEjemplos=0, validacion=None):
    arbol = entrenador(conjunto, medida, maxFrecuencia, minEjemplos)
    return entrenadorPodaRec(arbol,validacion,rendimiento=0.0)

'''idea: coger los caminos, reordenarlos de mayor a menor, crear un nuevo
arbol con cada camino, si el arbol es mejor que el anterior, se vuelven
a coger los caminos y asi continuamente hasta que la lista de caminos sea
0'''

def entrenadorPodaRec(arbol, validacion, rendimiendo):
    arbolFinal = copy.deepcopy(arbol)
    
    if arbolFinal.ramas != None:
        x = arbolFinal.ramas
        for rama in x:
            if x[rama].ramas == None:
                None
            else:
                x = x[rama].ramas
    
    #if arbol.ramas != None:
    return arbolFinal

'''La función nodosInterioresRec devuelve una lista de listas de cada
camino que se puede formar en el árbol con los nodos interiores hasta
los nodos hoja.'''

def nodosInterioresRec(arbol,ramasNodo=None):
    res = list()
    if arbol.ramas != None:
        for rama in arbol.ramas:
            if ramasNodo == None:
                resAux = list()
            else:
                resAux = list(ramasNodo)
            resAux.append(rama)
            res.append(resAux)
            siguienteNodo = nodosInterioresRec(arbol.ramas[rama],resAux)
            if siguienteNodo != None:
                resAux = list()
                for x in siguienteNodo:
                    resAux.append(x)
                res = res + resAux
        return res
    else:
        return None
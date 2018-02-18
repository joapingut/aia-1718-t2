# -*- coding: utf-8 -*-
from ClasificadorDT import clasificador, evaluador, imprimir
from utils import Clasificador, NodoDT, ClasificadorNoEntrenado

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
    None
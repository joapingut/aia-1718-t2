# -*- coding: utf-8 -*-

from clasificadores.clasificador import Clasificador, ClasificadorNoEntrenado
from clasificadores.utils import proporcionClase
import math, operator

'''ClasificadorDT es subclase de Clasificador, a lo que se añade
un campo entrenado que indica si el entrenamiento se ha realizado,
en caso negativo, se devuelve una excepción ClasificadorNoEntrenado.'''

class ClasificadorDR(Clasificador):

    def __init__(self, clasificacion, clases, atributos):
        super().__init__(clasificacion, clases, atributos)
        self.entrenado = False

    def entrena(self, entrenamiento):
        self.entrenamiento = entrenamiento
        self.arbol = entrenador(self.entrenamiento)
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

class ReglaDR():

    def __init__(self, categoria):
        self.categoria = categoria
        self.reglas = []

    def addRule(self, atributo):
        self.reglas.append(atributo)

    def getRules(self):
        return self.reglas

    def getCategoria(self):
        return self.categoria

def entrenador (entrenaminto):
    proporciones = proporcionClase(entrenaminto, True)
    clases_ord =  sorted(proporciones.items(), key=operator.itemgetter(1), reverse=True)
    examples = None;
    actual = []
    rule =[]
    while actual.count() is not 0:
        None
    None

def clasificador(ejemplo, reglas):
    None

def evaluador(prueba, reglas):
    None

def imprimir(reglas):
    None
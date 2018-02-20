# -*- coding: utf-8 -*-

from clasificadores.clasificador import Clasificador, ClasificadorNoEntrenado
from clasificadores.utils import proporcionClase, ejemplosClase
import math, operator, copy

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

    ''' Ejemplo de elemento ['n','s','n','s','s','s','n','n','n','s','?','s','s','s','n','s','republicano']'''
    def evalutate(self, elemento, positivo=True):
        clase = elemento[-1]
        if positivo and self.categoria != clase:
            return False
        for atributo, valor in self.reglas:
            if elemento[atributo] != valor:
                return False
        return True

    def getFrecuenciaRelativa(self, conjunto):
        return self.getCountPositivos(conjunto) / self.getCountValidos(conjunto)

    def getCountPositivos(self, conjunto):
        count = 0
        for elemento in conjunto:
            if self.evalutate(elemento, True):
                count += 1
        return count

    def getCountValidos(self, conjunto):
        count = 0
        for elemento in conjunto:
            if self.evalutate(elemento, False):
                count += 1
        return count

    def __str__(self):
        return "Regla: " + str(self.categoria) + " condiciones: " + str(self.reglas)

def entrenador (entrenaminto, atributos):
    proporciones = proporcionClase(entrenaminto, True)
    clases_ord =  sorted(proporciones.items(), key=operator.itemgetter(1), reverse=False)
    #examples = getDictOfExamples(entrenaminto, proporciones.keys())
    reglas = []
    for clase, puntuacion in clases_ord[0:len(clases_ord) - 1]:
        reglas_clase = entrena_clase(clase, entrenaminto, atributos)
        reglas.extend(reglas_clase)
    reglas.append(ReglaDR(clases_ord[-1][0]))
    return reglas

def entrena_clase(clase, entrenamiento, atributos):
    rules = []
    ejemplos = copy.copy(entrenamiento)
    while len(ejemplos) > 0:
        rule = ReglaDR(clase)
        rule = entrena_regla(rule, ejemplos, atributos)
        rules.append(rule)
        ejemplos = removeCubiertos(ejemplos, rule)
    return rules

def entrena_regla(rule, entrenamiento, atributos):
    cubiertos = entrenamiento
    while rule.getFrecuenciaRelativa(cubiertos) > 0 and rule.getFrecuenciaRelativa(cubiertos) < 1:
        rule = ampliar_regla(rule, atributos, cubiertos)
        cubiertos = removeNoCubiertos(cubiertos, rule)
    return rule

def ampliar_regla(regla, atributos, entrenamiento):
    sorted_atributes = proporcionAtributos(regla, atributos, entrenamiento)
    nuevo = (sorted_atributes[0][0], sorted_atributes[0][1])
    regla.addRule(nuevo)
    return regla

def proporcionAtributos(regla, atributos, entrenamiento):
    i = 0
    resultado = []
    for atributo, valores in atributos:
        for valor in valores:
            total = 0
            cumplen = 0
            for elemento in entrenamiento:
                ejemplo = elemento[i]
                if ejemplo == valor:
                    total += 1
                    if elemento[-1] == regla.getCategoria():
                        cumplen += 1
            if total != 0:
                resultado.append((i, valor, cumplen/total, cumplen))
        i += 1
    return sorted(resultado, key=operator.itemgetter(2), reverse=True)

def removeNoCubiertos(elementos, regla):
    cubiertos = []
    for elemento in elementos:
        if regla.evalutate(elemento, positivo=False):
            cubiertos.append(elemento)
    return cubiertos

def removeCubiertos(elementos, regla):
    noCubiertos = []
    for elemento in elementos:
        if not regla.evalutate(elemento, positivo=False):
            noCubiertos.append(elemento)
    return noCubiertos

def getGanancia(entrenamiento, rule, cadidate):
    fr_base = rule.getFrecuenciaRelativa(entrenamiento)
    fr_candidata = cadidate.getFrecuenciaRelativa(entrenamiento)
    p_base = rule.getCountPositives(entrenamiento)
    return p_base * (math.log2(fr_candidata) - math.log2(fr_base))

def getDictOfExamples(conjunto, clases):
    result = {}
    for clase in clases:
        result[clase] = ejemplosClase(conjunto, clase)
    return result

def clasificador(ejemplo, reglas):
    None

def evaluador(prueba, reglas):
    None

def imprimir(reglas):
    None
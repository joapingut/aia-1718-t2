# -*- coding: utf-8 -*-

from clasificadores.clasificadorDR import ClasificadorDR, ReglaDR
import copy

'''
ClasificadorDRPoda es una clase que hereda de ClasificadorDR que funciona igual
salvo porque despues de entrenar realiza una postpoda de las reglas.
'''
class ClasificadorDRPoda(ClasificadorDR):

    def __init__(self, clasificacion, clases, atributos):
        super().__init__(clasificacion, clases, atributos)

    ''' ClasificadorDRPoda recibe ademas del conjunto de entrenamiento
        otro conjunto de validacion para realizar la poda. '''
    def entrena(self, entrenamiento, validacion):
        super().entrena(entrenamiento)
        self.reglas = podarReglas(self, validacion)

    def clasifica(self, ejemplo):
        return super().clasifica(ejemplo)

    def evalua(self, prueba):
        return super().evalua(prueba)

    def imprime(self):
        return super().imprime()

    def get_reglas(self):
        return super().get_reglas()

    def set_reglas(self, reglas, entrenado=True):
        super().set_reglas(reglas, entrenado)

''' Metodo usado por el ClasificadorDRPoda para realizar la poda.
    Se encarga de ir eliminado condiciones de las reglas del clasificador
    hasta que no sea posible eliminar ninguna más. Tras terminar devuelve el
    mejor conjunto de reglas que puede ser el original si no hemos mejorado nada. '''
def podarReglas(clasificador, validacion):
    maximun = clasificador.evalua(validacion)
    clasificadorPruebas = copy.deepcopy(clasificador)
    originales = copy.deepcopy(clasificador.reglas)
    bestChoice = copy.deepcopy(clasificador.reglas)
    i = len(originales) - 2
    while i >= 0:
        original = originales[i]
        regla = eliminarCondicionRegla(original)
        if regla == None:
            del originales[i]
            i -= 1
        else:
            originales[i] = regla
        clasificadorPruebas.set_reglas(originales)
        candidate = clasificadorPruebas.evalua(validacion)
        if candidate >= maximun:
            maximun = candidate
            bestChoice = copy.deepcopy(clasificadorPruebas.reglas)
    return bestChoice

''' Metodo que dada una regla elimina la ultima condicion de la misma o devuelve None si
    la regla ya no tiene mas condiciones. '''
def eliminarCondicionRegla(regla):
    if len(regla.reglas) > 0:
        del regla.reglas[-1]
        return regla
    return None
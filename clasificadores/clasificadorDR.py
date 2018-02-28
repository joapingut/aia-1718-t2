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
        self.reglas = []

    def entrena(self, entrenamiento):
        self.entrenamiento = entrenamiento
        self.reglas = entrenador(self.entrenamiento, self.atributos)
        self.entrenado = True

    def clasifica(self, ejemplo):
        if self.entrenado:
            return clasificador(ejemplo,self.reglas)
        else:
            return ClasificadorNoEntrenado(Exception)

    def evalua(self, prueba):
        if self.entrenado:
            aciertos = 0;
            for instancia in prueba:
                evaluacion = evaluador(instancia,self.reglas)
                if evaluacion == instancia[-1]:
                    aciertos += 1
            return  aciertos / len(prueba)
        else:
            return ClasificadorNoEntrenado(Exception)

    def imprime(self):
        if self.entrenado:
            return imprimir(self.reglas, self.atributos)
        else:
            return ClasificadorNoEntrenado(Exception)

    def get_reglas(self):
        return self.reglas

    def set_reglas(self, reglas, entrenado=True):
        self.reglas = reglas
        self.entrenado = entrenado

'''
ReglaDR es una clase que nos permite encapsular la implementacion
de una regla.
Las reglas están implementadas como una lista de tuplas donde el primer valor
es la posicion del atributo en la lista de atributos y el segundo es el valor
de dicho atributo para esta regla. EJ: [(0, 'adulto'), (1,'1st')].
'''
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

    ''' Metodo que dado un elemento de un conjunto evalua las condiciones de
    esta regla para ese elemento.
    Si el parametro positivo es True se mira primero que la clase esperada para el
    elemento sea del mismo tipo que precide esta regla. Esto es importante para el
    calculo de la frecuencia relativa durante la fase de entrenamiento.'''
    def evaluate(self, elemento, positivo=False):
        clase = elemento[-1]
        if positivo and self.categoria != clase:
            return False
        for atributo, valor in self.reglas:
            if elemento[atributo] != valor:
                return False
        return True

    def getFrecuenciaRelativa(self, conjunto):
        return self.getCountPositivos(conjunto) / self.getCountValidos(conjunto)

    ''' Metodo que devuelve el numero de elementos que cumplen la regla y ademas
    poseen la misma clase que precide la regla'''
    def getCountPositivos(self, conjunto):
        count = 0
        for elemento in conjunto:
            if self.evaluate(elemento, True):
                count += 1
        return count

    ''' Metodo que devuelve el numero de elementos de un conjunto que cumplen la regla
    aunque la prediccion de la clase no sea la esperada.'''
    def getCountValidos(self, conjunto):
        count = 0
        for elemento in conjunto:
            if self.evaluate(elemento, False):
                count += 1
        return count

    def __str__(self):
        return "Regla: " + str(self.categoria) + " condiciones: " + str(self.reglas)

''' Metodo para apartir de un conjunto de entrenamiento y otro de atributos genera una serie de reglas
    que se ajustan a dicho conjunto de entranmiento. Estas reglas seran usada luego para iniciar el
    clasificador. '''
def entrenador (entrenaminto, atributos):
    proporciones = proporcionClase(entrenaminto, True)
    clases_ord =  sorted(proporciones.items(), key=operator.itemgetter(1), reverse=False)
    reglas = []
    for clase, puntuacion in clases_ord[0:len(clases_ord) - 1]:
        reglas_clase = entrena_clase(clase, entrenaminto, atributos)
        reglas.extend(reglas_clase)
    reglas.append(ReglaDR(clases_ord[-1][0]))
    return reglas

''' Metodo usado para generar reglas segun una clase. Por ejemplo, para la clase reuplicando este metodo
    generara una serie de reglas que describen quien es republicano en base a los datos del conjunto de
    entrenamiento.'''
def entrena_clase(clase, entrenamiento, atributos):
    rules = []
    ejemplos = copy.copy(entrenamiento)
    while len(ejemplos) > 0:
        rule = ReglaDR(clase)
        rule = entrena_regla(rule, ejemplos, atributos)
        if len(rule.getRules()) > 0:
            rules.append(rule)
        ejemplos = removeCubiertos(ejemplos, rule)
    return rules

''' Metodo que entrena una regla a partir del conjunto de entrenamiento pasado añadiendole nuevas condiciones.'''
def entrena_regla(rule, entrenamiento, atributos):
    cubiertos = entrenamiento
    attr_used = set()
    while len(attr_used) < len(atributos) and rule.getFrecuenciaRelativa(cubiertos) > 0 and rule.getFrecuenciaRelativa(cubiertos) < 1:
        rule = ampliar_regla(rule, atributos, cubiertos, attr_used)
        cubiertos = removeNoCubiertos(cubiertos, rule)
    return rule

''' Metodo para añadir una nueva condicion a una regla en base a los atributos que aun no hemos usado
    y a la proporcion de los mismos siendo preferente los que clasifican menos ejemplos (los mas concretos)
    y de ahí pasamos a los mas generales. '''
def ampliar_regla(regla, atributos, entrenamiento, attr_used):
    sorted_atributes = ordena_por_elementos(proporcionAtributos(regla, atributos, entrenamiento))
    for i in range(0, len(sorted_atributes)):
        if not(sorted_atributes[i][0] in attr_used):
            nuevo = (sorted_atributes[i][0], sorted_atributes[i][1])
            regla.addRule(nuevo)
            attr_used.add(sorted_atributes[i][0])
            break
    return regla

''' Metodo que dada una regla, una lista de atributos y un conjunto calcula la proporcion de los atributos.
    El resultado devuelto tiene esta forma (A, B, C, D) siendo:
    A: el indice del atributo elegido
    B: el valor del atributo elegido
    C: procentaje de las instancias que cumplen (tienen ese atributo con ese valor) partido el total
    D: numero de instancias que cumplen (tienen ese atributo con ese valor)'''
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

''' Funcion para ordernar una lista de elementos por numero de instancias clasificadas correctamente.
    Se usa con la salida de la funcion proporcionAtributos. Si dos elementos tiene la misma C se pone primero
    el que tenga mayor D.
'''
def ordena_por_elementos(conjunto):
    if conjunto == None or len(conjunto) < 2:
        return conjunto
    for i in range(0, len(conjunto) - 1):
        elemento = conjunto[i]
        siguiente = conjunto[i + 1]
        if elemento[2] == siguiente[2]:
            if elemento[3] < siguiente[3]:
                conjunto[i] = siguiente
                conjunto[i + 1] = elemento
    return conjunto

''' Metodo que dado un conjunto de instancias y una regla elimina del conjunto los que no esten
    cubiertos por dicha regla (no la cumplen). '''
def removeNoCubiertos(elementos, regla):
    cubiertos = []
    for elemento in elementos:
        if regla.evaluate(elemento, positivo=False):
            cubiertos.append(elemento)
    return cubiertos

''' Metodo que dado un conjunto de instancias y una regla elimina del conjunto los que esten
    cubiertos por dicha regla (la cumplen). '''
def removeCubiertos(elementos, regla):
    noCubiertos = []
    for elemento in elementos:
        if not regla.evaluate(elemento, positivo=False):
            noCubiertos.append(elemento)
    return noCubiertos

''' Metodo que dado un conjunto, una regla y otra regla candidata calcula la ganancia de la regla candidata. '''
def getGanancia(entrenamiento, rule, cadidate):
    fr_base = rule.getFrecuenciaRelativa(entrenamiento)
    fr_candidata = cadidate.getFrecuenciaRelativa(entrenamiento)
    p_base = rule.getCountPositives(entrenamiento)
    return p_base * (math.log2(fr_candidata) - math.log2(fr_base))

''' Metodo que llama el clasificador para realizar la clasificacion de un ejemplo. '''
def clasificador(ejemplo, reglas):
    return evaluador(ejemplo, reglas)

''' Metodo que llama el clasificador para evaludar un elemento. '''
def evaluador(prueba, reglas):
    for regla in reglas:
        if regla.evaluate(prueba):
            return regla.getCategoria()
    return None

''' Metodo que devuelve uan cadena con una representacion de las reglas pasadas. '''
def imprimir(reglas, atributos):
    result = ''
    for regla in reglas[:-1]:
        aux = '('
        for condicion in regla.reglas:
            aux += '(' + str(atributos[condicion[0]][0]) + '=' + str(condicion[1]) + ') /\ '
        aux = aux[:-4]
        aux += ') -> ' + regla.getCategoria()
        result += '\n' + aux
    result = result[1:] + '\nEn otro caso -> ' + reglas[-1].getCategoria()
    return result
# -*- coding: utf-8 -*-
import copy
from clasificadores.clasificadorDT import clasificador, evaluador, imprimir, entrenador
from clasificadores.clasificador import Clasificador, ClasificadorNoEntrenado

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
        self.arbol = entrenadorPoda(self.entrenamiento,self.medida,self.maxima_frecuencia,self.minimo_ejemplos,self.validacion,self.atributos)
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
        
def entrenadorPoda(conjunto, medida="entropia", maxFrecuencia=1, minEjemplos=0, validacion=None,atributos):
    arbol = entrenador(conjunto, medida, maxFrecuencia, minEjemplos)
    return entrenadorPodaRec(arbol,validacion,atributos)

'''El entrenadorPodaRec coge todos los posibles caminos a los nodos interiores, 
los reordena de mayor a menor tamaño, cambia el último nodo de cada camino a uno hoja, 
crea un nuevo árbol y, si el árbol tiene mejor rendimiento que el anterior, se vuelven
a coger los caminos para este nuevo árbol y así continuamente hasta que se recorran
todos los caminos sin encontrar un mejor árbol.'''

def entrenadorPodaRec(arbol, validacion,atributos,rendimiento=0.0):
    arbolCopia = copy.deepcopy(arbol)
    caminos = nodosInterioresRec(arbolCopia)
    caminos = caminosATratar(arbolCopia,caminos)
    caminos.sort(key = len, reverse = True)

    for camino in caminos:
        arbolCandidato = copy.deepcopy(arbolCopia)
        ultimoN = ultimoNodo(arbolCandidato,camino)
        ultimoN.atributo = None
        ultimoN.clase = max(ultimoN.distr,key=ultimoN.distr.get)
        ultimoN.ramas = None
        rendimientoCandidato = evaluador(validacion,arbolCandidato)
        if rendimientoCandidato >= rendimiento:
            arbolFinal = copy.deepcopy(arbolCandidato)
            arbolCopia = copy.deepcopy(arbolCandidato)
            caminos = nodosInterioresRec(arbolFinal)
            caminos = caminosATratar(arbolFinal,caminos)
            caminos.sort(key = len, reverse = True)
            rendimiento = rendimientoCandidato
    
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

'''La función caminosATratar recorre todos los caminos posibles del árbol
y los procesa para solo quedarnos con los caminos a los nodos interiores
para podar.'''

def caminosATratar(arbol,caminos):
    caminosCopia = list(caminos)
    for camino in caminos:
        if comprobarCamino(arbol,camino) != None:
            caminosCopia.remove(camino)
    return caminosCopia

'''La función comprobarCamino comprueba si un camino del árbol lleva a un nodo
hoja o no.'''

def comprobarCamino(arbol,camino):
    arbolCopia = copy.deepcopy(arbol)
    for indice in range(len(camino)):
        if indice != len(camino):
            rama = arbolCopia.ramas[camino[indice]]
            if comprobarNodo(rama):
                return rama.clase
            arbolCopia = rama

'''La función comprobarNodo devuelve un booleano dependiendo de si tiene un
valor de clase o no. Comprueba si un nodo es hoja o interior.'''            

def comprobarNodo(arbol):
    if arbol.clase == None:
        return False
    else:
        return True

'''La función ultimoNodo devuelve el último nodo de un camino del árbol
hacia un nodo interior.'''

def ultimoNodo(arbol,camino):
    for indice in range(len(camino)):
        if indice != len(camino):
            rama = arbol.ramas[camino[indice]]
            arbol = rama
    return arbol
# -*- coding: utf-8 -*-

'''
Clasificador es la clase básica que describe un clasificador sobre la que se implementaran el resto de clasificadores.
'''
class Clasificador:
    def __init__(self,clasificacion,clases,atributos):
        self.clasificacion=clasificacion
        self.clases=clases
        self.atributos=atributos
    def entrena(self,entrenamiento,validacion=None):
        pass
    def clasifica(self,ejemplo):
        pass
    def evalua(self,prueba):
        pass
    def imprime(self):
        pass

'''
NodoDT es una clase que describe los atributos que posee un nodo de un arbol usado por los clasificadores.
'''
class NodoDT(object):
    def __init__(self,atributo=-1,distr=None,ramas=None,clase=None):
        self.distr=distr
        self.atributo=atributo
        self.ramas=ramas
        self.clase=clase
        

'''
Clase que lanza una excepción. Usada para cuando un clasificador no esta entrenado aún.
'''
class ClasificadorNoEntrenado(Exception): pass
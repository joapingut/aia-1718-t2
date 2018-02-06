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


class NodoDT(object):
    def __init__(self,atributo=-1,distr=None,ramas=None,clase=None):
        self.distr=distr
        self.atributo=atributo
        self.ramas=ramas
        self.clase=clase
        

class ClasificadorNoEntrenado(Exception): pass
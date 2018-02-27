# -*- coding: utf-8 -*-
from clasificadores.clasificador import Clasificador, NodoDT, ClasificadorNoEntrenado
from clasificadores.utils import proporcionClase, subconjuntoValorAtributo
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
        self.arbol = entrenador(self.entrenamiento,self.medida,self.maxima_frecuencia,self.minimo_ejemplos,self.atributos)
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
            return imprimir(self.arbol,self.atributos)
        else:
            return ClasificadorNoEntrenado(Exception)

'''La función medidas realiza la función que se utilizará
para cuantificar el grado de clasificación dependiendo de la
medida que entre como entrada.'''

def medidas(medida, conjunto):
    result = 0.0
    if medida=="entropia":
        proporcionClases = proporcionClase(conjunto,True)
        for p in proporcionClases:
            result = result + proporcionClases[p]*math.log2(proporcionClases[p])
        result = -result
        
    elif medida=="error":
        proporcionClases = proporcionClase(conjunto)
        result = 1 - proporcionClases[max(proporcionClases, key=proporcionClases.get)] / len(conjunto)
    
    elif medida=="gini":
        proporcionClases = proporcionClase(conjunto,True)
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

def proporcionEjemplo(conjunto, indice=0, valorAtributo=None, porcentaje=False):
    proporcion = dict()
    if valorAtributo == None:
        for x in conjunto:
            valor = x[indice]
            if valor not in proporcion.keys():
                proporcion[valor] = 1
            else:
                proporcion[valor] += 1
    else:
        for x in conjunto:
            valor = x[indice]
            if valor == valorAtributo and valor not in proporcion.keys():
                proporcion[valor] = 1
            elif valor == valorAtributo:
                proporcion[valor] += 1
    if porcentaje:
        for x in proporcion:
            proporcion[x] = proporcion[x]/len(conjunto)
    return proporcion

'''indiceAtributo devuelve un diccionario con todos los atributos
como clave y su posición en la lista como valor, para una entrada tal que: 
[('clase',['1st','2nd','3rd']),('edad',['niño','adulto']),('genero',['male','female'])],
el resultado sería {'clase': 0, 'edad': 1, 'genero': 2}.'''

def indiceAtributo(atributos):
    indices = dict()
    for atributo in atributos:
        indices[atributo[0]] = atributos.index(atributo)
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
        copiaEjemplo = list(ejemplo)
        clase = copiaEjemplo.pop()
        if clasificador(copiaEjemplo,arbol) == clase:
            aciertos += 1
    return aciertos/len(prueba)

'''La función imprimirRec devuelve una representación del árbol que
se pasa como parámetro de entrada a partir de los distintos subárboles
de sus ramas y la profundidad en el árbol. Se representa el valor de 
cada nivel de profundidad y el valor del atributo por cada rama, además
de una indentación que depende de la profundidad para una representación
más clara de las ramas. Si el nodo que se trata no tiene ramas, es un nodo
hoja y se representa el valor de clasificación.'''

def imprimirRec(arbol,atributos,profundidad):
    resultado = ""
    if arbol.ramas != None:
        for rama in arbol.ramas:
            resultado += "\n"+"\t"*profundidad+atributos[arbol.atributo][0]+": ("+str(rama)+")"+imprimirRec(arbol.ramas[rama],atributos,profundidad+1)
    else:
        resultado = " -> ["+arbol.clase+"]\n"
    return resultado

'''La función imprimir llama a imprimirRec, genera la cadena del árbol
y la imprime.'''

def imprimir(arbol,atributos,profundidad=0):
    arbolRes = imprimirRec(arbol,atributos,profundidad)
    print(arbolRes)

'''La función entrenador desarrolla el árbol de manera recursiva llamando
a la propia función variando el conjunto de entrada, y los atributos por
cada iteración. Para los casos en los que se trata de un nodo hoja, se realiza
una comprobación de la proporción de clases (si para el conjunto de entrada el
valor de clasificación es el mismo para todos los casos), de los atributos (si
no quedan más que estudiar) o si el conjunto de entrada es vacío (por lo que la
variable atributoElegido valdría None y se crearía un nodo hoja). En cualquier
otro caso, se trata de un nodo interior y se trata cada valor de los atributos
de entrada y se observa el mejor valor dependiendo de la medida, cogiendo el mínimo.
Es en ese bucle donde se realiza la comprobación de la máxima frecuencia y el mínimo
de ejemplos, en la cual si se cumple alguna, no se elige el atributo candidato'''

def entrenador(conjunto, medida, maxFrecuencia, minEjemplos, atributos, indices=None, claseMax=None):
    if indices == None:
        indices = indiceAtributo(atributos)
    valorMin = 100.0
    atributosCopia = list(atributos)
    proporcionClases = proporcionClase(conjunto)
    atributoElegido = None
    if len(proporcionClases) == 1 or indices == {} or atributosCopia == [] or len(conjunto) == 0:
        if proporcionClases == {}:
            arbol = NodoDT(None,proporcionClases,None,max(claseMax,key=claseMax.get))
        else:    
            arbol = NodoDT(None,proporcionClases,None,max(proporcionClases,key=proporcionClases.get))
        
    else:
        ramas = dict()
        for atributo in atributosCopia:
            nombreAtributo = atributo[0]
            valoresAtributo = atributo[1]
            medidaValor = 0.0
            for valor in valoresAtributo:
                subconjunto = subconjuntoValorAtributo(conjunto,indices[nombreAtributo],valor)
                medidaValor = medidaValor + medidas(medida,subconjunto)
                medidaValor = medidaValor*len(subconjunto)/len(conjunto)
                proporcionClaseSub = proporcionClase(subconjunto,True)
                if proporcionClaseSub != {}:
                    if medidaValor <= valorMin and proporcionClaseSub[max(proporcionClaseSub,key=proporcionClaseSub.get)] <= maxFrecuencia and len(subconjunto)/len(conjunto) >= minEjemplos:
                        atributoElegido = atributo
                        valorMin = medidaValor
        if atributoElegido == None:
            arbol = NodoDT(None,proporcionClases,None,max(proporcionClases,key=proporcionClases.get))
        else:
            atributosCopia.remove(atributoElegido)
            for valor in atributoElegido[1]:
                ramas[valor] = entrenador(subconjuntoValorAtributo(conjunto,indices[atributoElegido[0]],valor),medida,maxFrecuencia,minEjemplos,atributosCopia,indices,proporcionClases)
            arbol = NodoDT(indices[atributoElegido[0]],proporcionClases,ramas,None)
    return arbol
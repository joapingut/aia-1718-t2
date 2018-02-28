# -*- coding: utf-8 -*-
__author__ = 'Joaquin, Luis'

from clasificadores.clasificadorDT import *
from clasificadores.clasificadorDTPoda import *

import data.votos as Votos

import data.prestamos as Prestamos

import data.titanic as Titanic

#---------------------
# Pruebas para arboles
#---------------------

#---------------------
# Pruebas para Votos
#---------------------

arbol = ClasificadorDT(Votos.clasificacion,Votos.clases,Votos.atributos)

arbol.entrena(Votos.entrenamiento)

arbol.imprime()

arbol.evalua(Votos.prueba)

arbol.evalua(Votos.validacion)

arbol.clasifica(['s','s','s','n','n','?','s','s','s','s','n','n','n','n','s','?'])

arbol.clasifica(['?','s','n','n','n','n','s','s','s','s','s','n','n','s','s','s'])

arbolPoda = ClasificadorDTPoda(Votos.clasificacion, Votos.clases, Votos.atributos)

arbolPoda.entrena(Votos.entrenamiento,Votos.validacion)

arbolPoda.imprime()

arbolPoda.evalua(Votos.prueba)

arbolPoda.evalua(Votos.validacion)

#---------------------
# Pruebas para Prestamos
#---------------------

arbol = ClasificadorDT(Prestamos.clasificacion,Prestamos.clases,Prestamos.atributos)

arbol.entrena(Prestamos.entrenamiento)

arbol.imprime()

arbol.evalua(Prestamos.prueba)

arbol.evalua(Prestamos.validacion)

arbol.clasifica(['laboral','uno','una','ninguno','viudo','altos'])

arbol.clasifica(['parado','uno','una','uno','viudo','bajos'])

arbolPoda = ClasificadorDTPoda(Prestamos.clasificacion, Prestamos.clases, Prestamos.atributos)

arbolPoda.entrena(Prestamos.entrenamiento,Prestamos.validacion)

arbolPoda.imprime()

arbolPoda.evalua(Prestamos.prueba)

arbolPoda.evalua(Prestamos.validacion)

#---------------------
# Pruebas para Titanic
#---------------------

arbol = ClasificadorDT(Titanic.clasificacion,Titanic.clases,Titanic.atributos)

arbol.entrena(Titanic.entrenamiento)

arbol.imprime()

arbol.evalua(Titanic.prueba)

arbol.evalua(Titanic.validacion)

arbol.clasifica(['1st','adulto','female'])

arbol.clasifica(['2nd','niño','female'])

arbolPoda = ClasificadorDTPoda(Titanic.clasificacion, Titanic.clases, Titanic.atributos)

arbolPoda.entrena(Titanic.entrenamiento,Titanic.validacion)

arbolPoda.imprime()

arbolPoda.evalua(Titanic.prueba)

arbolPoda.evalua(Titanic.validacion)
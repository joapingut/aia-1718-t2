# -*- coding: utf-8 -*-
__author__ = 'Joaquin, Luis'

from clasificadores.clasificador import *
from clasificadores.clasificadorDT import *
from clasificadores.clasificadorDTPoda import *

import data.votos as Votos

import data.lentillas as Lentillas

import data.titanic as Titanic

import data.votos as Votos

import data.prestamos as Prestamos

import clasificadores.clasificadorDR as ClasifDR


#Clasificador Titanic

print(Titanic.clasificacion)
print(Titanic.clases)
print(Titanic.atributos)

clasificador_Titanic = ClasifDR.ClasificadorDR(Titanic.clasificacion, Titanic.clases, Titanic.atributos)

clasificador_Titanic.entrena(Titanic.entrenamiento)

print("Evaluacion: " + str(clasificador_Titanic.evalua(Titanic.validacion)))
print("Evaluacion pruebas: " + str(clasificador_Titanic.evalua(Titanic.entrenamiento)))
print(clasificador_Titanic.clasifica(['1st', 'adulto', 'male', '0']))
for regla in clasificador_Titanic.reglas:
    print(regla)



''' Ejecutar este archivo para hacer las pruebas '''

print(Lentillas.clasificacion)
print(Lentillas.clases)
print(Lentillas.atributos)

clasificador_reglas = ClasifDR.ClasificadorDR(Lentillas.clasificacion, Lentillas.clases, Lentillas.atributos)

clasificador_reglas.entrena(Lentillas.entrenamiento)

print("Evaluacion: " + str(clasificador_reglas.evalua(Lentillas.entrenamiento)))
for regla in clasificador_reglas.reglas:
    print(regla)

#Clasificador Votos

print(Votos.clasificacion)
print(Votos.clases)
print(Votos.atributos)

clasificador_votos = ClasifDR.ClasificadorDR(Votos.clasificacion, Votos.clases, Votos.atributos)

clasificador_votos.entrena(Votos.entrenamiento)

print("Validacion: " + str(clasificador_votos.evalua(Votos.validacion)))
print("Validacion pruebas: " + str(clasificador_votos.evalua(Votos.entrenamiento)))
for regla in clasificador_votos.reglas:
    print(regla)

#Clasificador Prestamos

print(Prestamos.clasificacion)
print(Prestamos.clases)
print(Prestamos.atributos)

clasificador_Prestamos = ClasifDR.ClasificadorDR(Prestamos.clasificacion, Prestamos.clases, Prestamos.atributos)

clasificador_Prestamos.entrena(Prestamos.entrenamiento)

print("Validacion: " + str(clasificador_Prestamos.evalua(Prestamos.validacion)))
print("Validacion pruebas: " + str(clasificador_Prestamos.evalua(Prestamos.entrenamiento)))
for regla in clasificador_Prestamos.reglas:
    print(regla)

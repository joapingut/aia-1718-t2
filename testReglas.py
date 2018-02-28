# -*- coding: utf-8 -*-
__author__ = 'Joaquin, Luis'

import data.titanic as Titanic

import data.votos as Votos

import data.prestamos as Prestamos

import clasificadores.clasificadorDR as ClasifDR
import clasificadores.clasificadorDRPoda as ClasifDRPoda


#---------------------
# Pruebas para reglas
#---------------------

#---------------------
# Pruebas para Titanic
#---------------------

print('Pruebas Titanic\nInformacion:')
print(Titanic.clasificacion)
print(Titanic.clases)
print(Titanic.atributos)

clasificador_Titanic = ClasifDR.ClasificadorDR(Titanic.clasificacion, Titanic.clases, Titanic.atributos)
clasificador_Titanic.entrena(Titanic.entrenamiento)

print("Evaluacion conjunto validacion: " + str(clasificador_Titanic.evalua(Titanic.validacion)))
print("Evaluacion conjunto de entrenamiento: " + str(clasificador_Titanic.evalua(Titanic.entrenamiento)))
print("Evaluacion conjunto de pruebas: " + str(clasificador_Titanic.evalua(Titanic.prueba)))
print("Prueba de clasificacion de un elemento, esperado 0, obtenido: " + str(clasificador_Titanic.clasifica(['1st', 'adulto', 'male', '0'])))
print("Reglas obtenidas:\n", str(clasificador_Titanic.imprime()))

# Titanic podado

clasificador_TitanicP = ClasifDRPoda.ClasificadorDRPoda(Titanic.clasificacion, Titanic.clases, Titanic.atributos)
clasificador_TitanicP.entrena(Titanic.entrenamiento, Titanic.validacion)

print('\n\nPruebas Titanic podado:')
print("Evaluacion conjunto validacion: " + str(clasificador_TitanicP.evalua(Titanic.validacion)))
print("Evaluacion conjunto de entrenamiento: " + str(clasificador_TitanicP.evalua(Titanic.entrenamiento)))
print("Evaluacion conjunto de pruebas: " + str(clasificador_TitanicP.evalua(Titanic.prueba)))
print("Prueba de clasificacion de un elemento, esperado 0, obtenido: " + str(clasificador_TitanicP.clasifica(['1st', 'adulto', 'male', '0'])))
print("Reglas obtenidas:\n", str(clasificador_TitanicP.imprime()))


#---------------------
# Pruebas para Votos
#---------------------

print('\n\nPruebas Votos\nInformacion:')
print(Votos.clasificacion)
print(Votos.clases)
print(Votos.atributos)

clasificador_votos = ClasifDR.ClasificadorDR(Votos.clasificacion, Votos.clases, Votos.atributos)
clasificador_votos.entrena(Votos.entrenamiento)

print("Evaluacion conjunto validacion: " + str(clasificador_votos.evalua(Votos.validacion)))
print("Evaluacion conjunto de entrenamiento: " + str(clasificador_votos.evalua(Votos.entrenamiento)))
print("Evaluacion conjunto de pruebas: " + str(clasificador_votos.evalua(Votos.prueba)))
print("Prueba de clasificacion de un elemento, esperado republicano, obtenido: "
      + str(clasificador_votos.clasifica(['n','s','n','s','s','s','n','n','n','n','n','s','s','s','n','n','republicano'])))
print("Reglas obtenidas:\n", str(clasificador_votos.imprime()))

# Votos podado

clasificador_votosP = ClasifDRPoda.ClasificadorDRPoda(Votos.clasificacion, Votos.clases, Votos.atributos)
clasificador_votosP.entrena(Votos.entrenamiento, Votos.validacion)

print('\n\nPruebas Votos podado:')
print("Evaluacion conjunto validacion: " + str(clasificador_votosP.evalua(Votos.validacion)))
print("Evaluacion conjunto de entrenamiento: " + str(clasificador_votosP.evalua(Votos.entrenamiento)))
print("Evaluacion conjunto de pruebas: " + str(clasificador_votosP.evalua(Votos.prueba)))
print("Prueba de clasificacion de un elemento, esperado republicano, obtenido: "
      + str(clasificador_votosP.clasifica(['n','s','n','s','s','s','n','n','n','n','n','s','s','s','n','n','republicano'])))
print("Reglas obtenidas:\n", str(clasificador_votosP.imprime()))


#---------------------
# Pruebas para Prestamos
#---------------------

print('\n\nPruebas Prestamos\nInformacion:')
print(Prestamos.clasificacion)
print(Prestamos.clases)
print(Prestamos.atributos)

clasificador_Prestamos = ClasifDR.ClasificadorDR(Prestamos.clasificacion, Prestamos.clases, Prestamos.atributos)
clasificador_Prestamos.entrena(Prestamos.entrenamiento)

print("Evaluacion conjunto validacion: " + str(clasificador_Prestamos.evalua(Prestamos.validacion)))
print("Evaluacion conjunto de entrenamiento: " + str(clasificador_Prestamos.evalua(Prestamos.entrenamiento)))
print("Evaluacion conjunto de pruebas: " + str(clasificador_Prestamos.evalua(Prestamos.prueba)))
print("Prueba de clasificacion de un elemento, esperado no conceder, obtenido: " + str(clasificador_Prestamos.clasifica(['laboral','uno','dos o más','dos o más','soltero','bajos','no conceder'])))
print("Reglas obtenidas:\n", str(clasificador_Prestamos.imprime()))

# Prestamos podado

clasificador_Prestamos_poda = ClasifDRPoda.ClasificadorDRPoda(Prestamos.clasificacion, Prestamos.clases, Prestamos.atributos)
clasificador_Prestamos_poda.entrena(Prestamos.entrenamiento, Prestamos.validacion)

print('\n\nPruebas Prestamos podado:')
print("Evaluacion conjunto validacion: " + str(clasificador_Prestamos_poda.evalua(Prestamos.validacion)))
print("Evaluacion conjunto de entrenamiento: " + str(clasificador_Prestamos_poda.evalua(Prestamos.entrenamiento)))
print("Evaluacion conjunto de pruebas: " + str(clasificador_Prestamos_poda.evalua(Prestamos.prueba)))
print("Prueba de clasificacion de un elemento, esperado no conceder, obtenido: " + str(clasificador_Prestamos_poda.clasifica(['laboral','uno','dos o más','dos o más','soltero','bajos','no conceder'])))
print("Reglas obtenidas:\n", str(clasificador_Prestamos_poda.imprime()))
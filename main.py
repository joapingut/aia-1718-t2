# -*- coding: utf-8 -*-
__author__ = 'Joaquin, Luis'

from clasificadores.clasificador import *
from clasificadores.clasificadorDT import *
from clasificadores.clasificadorDTPoda import *

import data.votos as Votos

import data.lentillas as Lentillas

import clasificadores.clasificadorDR as ClasifDR

''' Ejecutar este archivo para hacer las pruebas '''

for regla in ClasifDR.entrenador(Lentillas.entrenamiento, Lentillas.atributos):
    print(regla)
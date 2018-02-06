# -*- coding: utf-8 -*-
import csv

'''Código para procesar el conjunto de datos de supervivencia del titanic.
En vista de la información que da el archivo, hay datos que se pueden obviar
para los conjuntos finales ya que no son determinantes para la supervivencia
(como, por ejemplo, el nombre de cada persona de la tripulación), quedándonos
solo con la clase (si iba en 1ª, 2ª o en 3ª clase), con la edad (estableciendo
como límite de edad 13 para mayores y menores de edad, 0 para menores de 13 y 
1 para mayores de 13) y con el género como atributos, y como clase la supervivencia'''

#entrada "../aia-1718-t2/conjuntos de datos/titanic.txt"                  

#usar csv mejor

def procesamiento(archivo):
    reader = csv.DictReader(archivo)
    for row in reader:
        print(row['name'], row['age'])
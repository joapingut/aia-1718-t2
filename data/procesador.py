# -*- coding: utf-8 -*-
import csv

'''Código para procesar el conjunto de datos de supervivencia del titanic.
En vista de la información que da el archivo, hay datos que se pueden obviar
para los conjuntos finales ya que no son determinantes para la supervivencia
(como, por ejemplo, el nombre de cada persona de la tripulación), quedándonos
solo con la clase (si iba en 1ª, 2ª o en 3ª clase), con la edad (estableciendo
como límite de edad 13 para mayores y menores de edad, 0 para menores de 13 y 
1 para mayores de 13) y con el género como atributos, y como clase la supervivencia'''
                

'''La función procesaEjemplos tiene como parámetro de entrada el archivo titanic.txt
que tiene los datos separados por comas (csv), este formato permite una mejor manipulación
de los datos respecto a texto. Se guardan los ejemplos cuyas edades no sean desconocidas
(es decir, que no sean NA) en el resultado final y los ejemplos restantes (con edad = NA)
se guardan en una colección aparte para luego cambiar dichos valores por el valor
de edad media de los ejemplos guardados en el resultado final (si dicha media es
mayor que 13.0000, los valores de edad para esa colección será adulto, en caso contrario,
niño) y cada ejemplo que se cambie se añadirá al resultado final'''       
                                                               
def procesaEjemplos(archivo):
    ejemplos = []
    conjuntoEdadAProcesar = []
    edadMediaTotal = 0.0
    with open(archivo,'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            if line[0] == "row.names":
                continue
            linea = []
            if line[4] != "NA":
                linea.append(line[1]) #clase
                linea.append(categoriaEdad(line[4])) #edad
                edadMediaTotal += float(line[4]) 
                linea.append(line[10]) #genero
                linea.append(line[2]) #supervivencia
                ejemplos.append(linea)
            else:
                linea.append(line[1])
                linea.append(line[4])
                linea.append(line[10])
                linea.append(line[2])
                conjuntoEdadAProcesar.append(linea)
        edadMedia = edadMediaTotal/len(ejemplos)
        categoriaEdadMedia = categoriaEdad(edadMedia)
        for linea in conjuntoEdadAProcesar:
            linea[1] = categoriaEdadMedia
            ejemplos.append(linea)
    return ejemplos

'''La función generadorConjuntos recorre los ejemplos ya formateados de procesaEjemplos,
los ordena y a partir de dicha ordenación, coge cada porción de ejemplos diferenciados por
la supervivencia y el género, y coge un porcentaje predeterminado de dicha porción para asignarlo
 en cada conjunto (60% para entrenamiento, 20% para validación y 20% para prueba).'''

def generadorConjuntos(ejemplos):
    resultado = [[],[],[]] #0:entrenamiento, 1:validacion, 2:prueba
    listaAuxiliar = []
    ejemplos.sort()
    supervivencia = ejemplos[0][3]
    genero = ejemplos[0][2]
    for ejemplo in ejemplos:
        if (ejemplo[2] != genero or ejemplo[3] != supervivencia) and listaAuxiliar != []:
            resultado[0] += listaAuxiliar[:round(len(listaAuxiliar)*3/5)] #0.6 para entrenamiento
            resultado[1] += listaAuxiliar[round(len(listaAuxiliar)*3/5):round(len(listaAuxiliar)*3/5+len(listaAuxiliar)*1/5)] #0.2 para validacion
            resultado[2] += listaAuxiliar[round(len(listaAuxiliar)*3/5+len(listaAuxiliar)*1/5):] #0.2 para prueba
            genero, supervivencia, listaAuxiliar = ejemplo[2], ejemplo[3], []
        listaAuxiliar.append(ejemplo)
    return resultado

'''generadorTitanic hace uso de las funciones previamente implementadas y genera el archivo
titanic.py con el formato usado en el resto de conjuntos de datos'''

def generadorTitanic(archivo, path=None):
    ejemplos = procesaEjemplos(archivo)
    conjuntos = generadorConjuntos(ejemplos)
    dst = None
    if(path is not None):
        dst = path + 'titanic.py'
    else:
        dst = 'titanic.py'
    f = open(dst,'w', encoding='utf-8')
    f.write("# -*- coding: utf-8 -*-\n")
    f.write("atributos = [('clase',['1st','2nd','3rd']),('edad',['niño','adulto']),('genero',['male','female'])]\nclasificacion = 'Supervivencia'\nclases = ['1','0']\n")
    f.write("entrenamiento = "+str(conjuntos[0])+"\n")
    f.write("validacion = "+str(conjuntos[1])+"\n")
    f.write("prueba = "+str(conjuntos[2])+"\n")
    f.close()

'''Si la edad de entrada es mayor que 13.0, se devuelve 'adulto', en caso contrario, 'niño'.
La utilidad de esta función es facilitar el paso de los datos de edad al formato de los datos 
finales quese usarán en titanic.py'''

def categoriaEdad(edad):
    if(float(edad)>13.0):
        return "adulto"
    else:
        return "niño"

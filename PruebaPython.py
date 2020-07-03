# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:41:22 2019

@author: cristina rodriguez chamorro
dni: 77380999Y
"""

from datetime import datetime
from functools import reduce


#Creacion de los objetos Estacion y medida
"""
Para el desarrollo de la presente practica se han creado los objetos estacion y
medida. De manera que, el objeto estacion esta formado por un id y una lista de
medidas. Por otro lado, la medida, esta formada por tres valores: fecha, presion y
temperatura.Ya que aunque el fichero a leer contenga mas informacion sobre las medidas,
solo interesan esos valores especificos para el desarrollo de la practica.

"""
#Construccion del objeto estacion
class Estacion(object):
    def __init__(self, id, listaMedidas):
        self.id = id
        self.listaMedidas = listaMedidas
       
    def __str__(self):
        return "[Id: " + str(self.id) + "]" + " [Medidas: " + Estacion.toString(self) + "]"
    
    def toString(self):
        return ' '.join([str(elem) for elem in self.listaMedidas])
    
#Construccion del objeto medidas      
class Medidas(object):
        def __init__(self, fecha, temperatura, presion):
            self.fecha = fecha
            self.temperatura = float(temperatura)
            self.presion = float(presion)
        def __str__(self):
           return ("[fecha: " + str(self.fecha)+ "," + " temperatura: " + \
        str(self.temperatura) + "," + " presion: " + str(self.presion) +"]")

#Lectura del fichero
    
def funcionLecturaFichero(fichero):
    listaEstaciones = []    
    try:
        with open(fichero) as f:
            for line_data in f:
                line_str = line_data.split()
                #De la linea que ha leido, se contruye un objeto medida con la fecha, temperatura y presion.
                listaMedidas = [Medidas(line_str[2],line_str[3], line_str[7])]
                encontrado = False
                #Recorremos las estaciones porque si hay una estacion que tenga mas de una medida, queremos incluirla en la lista de medidas de esa estacion.
                for est in listaEstaciones:
                    if(est.id == line_str[0]):
                        est.listaMedidas.append(Medidas(line_str[2],line_str[3], line_str[7]))
                        encontrado = True
                        break
                #En caso de que la estacion no haya aparecido ninguna vez, se tendra que incluir en la lista de estacioes.
                if(encontrado == False):
                    estacion = Estacion(line_str[0], listaMedidas)
                    listaEstaciones.append(estacion)
    except:
        #Si hubiese algun error en la lectura del fichero, aparecera un error como el que se puede ver a continuacion.
        print("ERROR: LA LECTURA DEL FICHERO NO ESTA SIENDO CORRECTA")
        
    return listaEstaciones    

#Creacion de metodos

#Ejercicio 1   

def funcionContador(estacion):
    """
    Lo que se hace en esta funcion es recibir una estacion y comprobar en su lista de medidas si la presion
    y la temperatura tienen valores correctos. De ser asi, cada aparicion correcta sumara uno al contador.
    
    """
    contador = 0         
    for medida in estacion.listaMedidas:
        if(medida.presion != 9999.9 and medida.temperatura != 9999.9):
            contador +=1
    return contador  

def contadorFilas(listaEstaciones):
    
    """
    Esta funcion hara uso de un map, que sera el que llame a la funcion anterior para enviar una estacion cada vez.
    Gracias a esto, el list(map()) nos devuelve una lista con el numero de medidas correctas que tiene cada estacion. 
    Por esta razon, sera necesario el uso de reduce(), ya que este comando va a permitirnos sumar todos los elementos
    de la lista que se estan recibiendo del map.  
    
    """
    return reduce(lambda x, y: x + y, list(map(funcionContador,listaEstaciones)))

   
#Ejercicio 2
    
"""
En este ejercicio se va a verificar la estacion menos correcta. Para ello, se utilizaran 3 condicionales.
De manera que, si la temperatura y la presion tienen valores incorrectos, el contador sumara 2. Por el contrario,
si uno de los valores es incorrecto solo se sumara uno. 
Al mismo tiempo se ira almancenando en un diccionario la estacion determinada con su correspondiente contador. De tal forma que,
se podra recorrer todos los valores del diccionario buscando el mayor, para posteriormente devolver la clave del diccionario cuyo
indice se corresponda con el mayor encontrado.

"""

def estacionmenosCorrecta(listaEstaciones):
    dic = {}
    mayor = 0
    for estacion in listaEstaciones:
        cont = 0
        for medida in estacion.listaMedidas:
             if(medida.presion == 9999.9 and medida.temperatura == 9999.9):
                cont +=2
                dic[estacion] = cont
             elif(medida.presion == 9999.9 and medida.temperatura != 9999.9):
                cont +=1
                dic[estacion] = cont
             elif(medida.presion != 9999.9 and medida.temperatura == 9999.9):
                cont +=1
                dic[estacion] = cont
    
    #A continuacion, se busca el mayor valor o contador almacenado en el diccionario.
    for v in dic.values():
        if(v > mayor):
            mayor = v  
    #Se devuelve la estacion de mayor valor encontrado, que sera la estacion menos correcta
    return list(dic.keys())[list(dic.values()).index(mayor)]        
          

#Ejercicio 3
    
"""
En este ejercicio se han utilizado dos funciones. TemperaturamaxminEstacion, 
llamara a comprueba estacion para hacer posible la asignacion en un diccionario
de los valores de temperatura maximos y minimos de cada estacion.
De manera que, la funcion list(map()) del primer metodo comentado, devolvera dicho diccionario
con las medidas de interes solicitadas por el enunciado.
"""
            
def compruebaTemperatura(estacion):
    
    """
    En este metodo, se va a recorrer las medidas de cada estacion. Y va a ir 
    asignando en un diccionario, el id de la estacion, con su correspondiente 
    temperatura maxima y minima.
    
    """
    menor = 0
    mayor = 0
    dic = {}
    for medida in estacion.listaMedidas:
        #Si la temperatura es mayor que el maximo valor encontrado y la estacion tiene mas de una medida, se asigna el mayor.        
        if(medida.temperatura>mayor and len(estacion.listaMedidas) > 2):
            mayor = medida.temperatura
        #Si la temperatura no es mayor que el maximo valor encontrado pero la estacion tiene mas de dos medidas, se asigna el menor.            
        elif(len(estacion.listaMedidas)>2):
            menor = medida.temperatura
        #En caso contrario, se asigna el mismo valor encontrado al menor y al mayor.
        else:
            mayor = medida.temperatura
            menor = mayor
    dic[estacion.id] = [mayor,menor]
    return dic
    
def temperaturamaxminEstacion(listaEstaciones):
    """
    En este metodo, map llama a compruebaTemperatura. A dicha funcion, se le pasa un objeto estacion.
    Se obtendra una lista de estaciones, con el id de la estacion, y su correspondiente temperatura (maxima y minima)
    """
    return list(map(compruebaTemperatura,listaEstaciones))

#Ejercicio 4

"""
En este ejercicio se va a mostrar el identificador de cada estacion, junto con el mes de la estacion y su correspondiente temperatura.

"""
def compruebaEstacion(estacion):
    mes = 0
    dic = {}           
    listaValores = []
    encontrado = False
    mayor = 0
    #Se recorren las medidas de cada estacion
    for medida in estacion.listaMedidas:                     
        mes = datetime.strptime(str(medida.fecha), "%Y%m%d").month
        #Se reccorre la lista de valores que almacenara pequeñas listas con el mes y la temperatura.
        for i in listaValores:            
            #A continuacion, lo que se hace es comprobar si el mes almacenado en la lista coincide con el actual leido.
            #Si los valores coinciden y la temperatura almacenada es menor que la actual medida, se intercambia el valor de la temperatura por el mayor.
            if(i[0] == mes and i[1] < medida.temperatura):
                mayor = medida.temperatura
                i[1] = mayor
                encontrado = True
        #Se establece un encontrado a false, para controlar que no aparezcan los meses con la temperaturas repetidos.       
        if(encontrado == False):                
            listaValores.append([mes, medida.temperatura])
    #Se asigna el id de la estacion con su lista de valores correspondiente.           
    dic[estacion.id] = listaValores                            
    return dic

def temperaturaMeses(listaEstaciones):
    """
    En este metodo se hace uso de un map(), que llamara al metodo compruebaEstacion, para pasarle en cada iteraccion una estacion.
    """
    return list(map(compruebaEstacion,listaEstaciones))
#Main 
    
if __name__ == "__main__":
    estacionesLeidas = funcionLecturaFichero("sample.txt")
    #Número de filas con datos de temperatura y presión (ambos) correctos.
    print("Numero de filas con los datos de temperatura y presion correctos: ", contadorFilas(estacionesLeidas))
    print("La estacion con menor numero de datos correctos es: ", estacionmenosCorrecta(estacionesLeidas))
    print("La temperatura maxima y minima de cada estacion: ", temperaturamaxminEstacion(estacionesLeidas))
    print("Estaciones con sus meses, temperaturas maximas y minimas: ", temperaturaMeses(estacionesLeidas))



import random 
import time
from io import open
import os 


#Variables Globales

#En estos arrays se guardarán los datos de los archivos que servirán para calcular las probabilidades
arrayAccionesLeon = []
arrayAccionImpala = []
arrayLeonEnLamira = []
arrayDistanciaEntreAmbos = []

#numeroDeEventos = 20


#Definicmos al clase Proceso, esta nos ayudará a que el programa identifique si está en modo de entrenamiendo o no
class Proceso:

    def __init__(self):
        self.tipoDeEjecución = ""
        self.archivosCreados = True


#Definimos la clase León
class Leon:
    
    def __init__(self):
        self.estado = "Inicial"
        self.posicionInicial = 6 #puede ser 1,2,3,4,5,6,7,8
        self.zonaSegura = True
        self.zonasPeligrosas = []
        self.zonaParaAtacar = False
        self.distanciaRecorrida = 0

        self.PAtacarDependiendoLaPosicion = [ 0,0,0,0,0,0,0,0 ]

        self.PAvanzarEnMira = 0
        self.PAvanzarFueraDeMira = 0

        self.PEsconderseEnMira = 0
        self.PEsconderseFueraDeMira = 0

        self.PAtacarEnMira = 0
        self.PAtacarFueraDeMira = 0

    def avanzar(self):
        self.estado = "Avanzando"
        self.distanciaRecorrida += 1
        

    def esconderse(self):
         self.estado = "Escondido"

    def atacar(self):
         self.estado = "Atacando"

    def situarseEnLaPosicion(self, posicion):
         self.posicionInicial = posicion


#Definimos la clase Impala
class Impala:

    def __init__(self):
        self.estado = "Inicial"
        self.detectoPeligro = False
        

    def verIzquierda(self):
        self.estado = "Viendo a la izquierda"

    def verDerecha(self):
        self.estado = "Viendo a la derecha"
    
    def verFrente(self):
        self.estado = "Viendo al frente"

    def beberAgua(self):
        self.estado = "Bebiendo agua"

    def huir(self):
        self.estado = "Huyendo"


#Cremaos los objetos 
myLeon = Leon()
myImpala = Impala()
myProcesoActual = Proceso()


def restablecerValores():

    myLeon.estado = "Inicial"
    myImpala.estado = "Inicial"
    myLeon.distanciaRecorrida = 0
    arrayAccionesLeon.clear()
    arrayAccionImpala.clear()
    arrayAccionesLeon.clear()
    arrayDistanciaEntreAmbos.clear()

    myLeon.zonaSegura = True
    myLeon.zonasPeligrosas.clear()
    myLeon.zonaParaAtacar = False

    myLeon.PAvanzarEnMira = 0
    myLeon.PAvanzarFueraDeMira = 0

    myLeon.PEsconderseEnMira = 0
    myLeon.PEsconderseFueraDeMira = 0

    myLeon.PAtacarEnMira = 0
    myLeon.PAtacarFueraDeMira = 0



#Regresa -1 si no encontró el elemento y regresa la posición de el elemento si sí lo  encontró
def busqieda_binaria(arreglo, busqueda, izquierda, derecha):
    if izquierda > derecha:
        return -1
    indiceDelElementoDelMedio = (izquierda + derecha) // 2
    elementoDelMedio = arreglo[indiceDelElementoDelMedio]
    if elementoDelMedio == busqueda:
        return indiceDelElementoDelMedio
    if busqueda < elementoDelMedio:
        return busqieda_binaria(arreglo, busqueda, izquierda, indiceDelElementoDelMedio - 1)
    else:
        return busqieda_binaria(arreglo, busqueda, indiceDelElementoDelMedio + 1, derecha)



def llenarArraysGlobales():

    #Limpiamos los arrays para evitar redundancias en la información.
    arrayAccionesLeon.clear()
    arrayAccionImpala.clear()
    arrayLeonEnLamira.clear()
    arrayDistanciaEntreAmbos.clear()


    #Abrir los archivos  y asignarlos a los arrays que están artiba
    archivoTexto = open("AccionesLeon.txt","r")
    array1 = archivoTexto.readlines()
    archivoTexto.close()

    archivoTexto2 = open("AccionesImpala.txt","r")
    array2 = archivoTexto2.readlines()
    archivoTexto2.close()

    archivoTexto3 = open("LeonEnLaMira.txt","r")
    array3 = archivoTexto3.readlines()
    archivoTexto3.close()

    archivoTexto4 = open("DistanciEntreAmbos.txt","r")
    array4 = archivoTexto4.readlines()
    archivoTexto4.close()

    #copiamos los datos a los arreglos globales
    for item in array1:
        arrayAccionesLeon.append(item)

    for item in array2:
        arrayAccionImpala.append(item)

    for item in array3:
        arrayLeonEnLamira.append(item)

    for item in array4:
        arrayDistanciaEntreAmbos.append(item)


#Se cálculan la probabilidades que el león tomará 
def CalcularProbabilidades():
    
    vecesQueHuyoEImpala = 0
    posicionesParaVerificar = []

    posicionesMenorQue2Cuadros = []

    vecesHuirPorAvanzarEnMira = 0
    vecesHuirPorAvanzarFueraDeMira = 0

    vecesHuirPorEsconderseEnMira = 0
    vecesHuirPorEsconderseFueraDeMira = 0

    vecesHuirPorAtacarEnMira = 0
    vecesHuirPorAtacarFueraDeMira = 0


    #Probabilidad de avanzar
    probabilidadHuirPorAvanzarEnMira = 0
    probabilidadHuirPorAvanzarFueraDeMira = 0

    #Probabilidad de esconderse
    probabilidadHuirPorEsconderseEnMira = 0
    probabilidadHuirPorEsconderseFueraDeMira = 0

    #Probabilidad de atacar
    probabilidadHuirPorAtacarEnMira = 0
    probabilidadHuirPorAtacarFueraDeMira = 0

    #Probabilidades de u ataque exitoso
    vecesQueMurio = []
    contadorPorPosicion = [ 0,0,0,0,0,0,0,0 ]
    PAtaqueExitosoEnLaPosicion = [ 0,0,0,0,0,0,0,0 ]



    llenarArraysGlobales()

    
    #Tenemos que conocer cuántas veces huyó el Impala
    i = 0
    for item in arrayAccionImpala:
        if item == "Huyendo\n" or item == "Huyendo":
            vecesQueHuyoEImpala += 1
            posicionesParaVerificar.append(i)
        i += 1

    #print("El array entero es: ",arrayAccionImpala)
    #print("\n\n\nLas veces que huyó el Impala fueron: ", vecesQueHuyoEImpala)
    #print("Las posiciones son: ", posicionesParaVerificar)
     






    #Hay que verificar cuantas veces huyó el impala por que el león estaba a menos de 2 cuadros de distancia
    #Si no verificamos eso nos va a producir errores en la información
    """for i in posicionesParaVerificar:

        if int(arrayDistanciaEntreAmbos[ i - 1 ]) < 3:
            posicionesMenorQue2Cuadros.append(int(arrayDistanciaEntreAmbos[ i - 1 ]))

    print("Las posiciones que huyó por que la distancia es menor a 3 son: ",posicionesMenorQue2Cuadros)"""




    #  *****************************************************************************************
    #¿Cuál es la probabilidad que huya dado que el león avanzó?
    #Hay que revisar en los otros dos arreglos pero en una posición antes
    for i in posicionesParaVerificar:

        if arrayLeonEnLamira[ i - 1 ] == "Si\n" or arrayLeonEnLamira[ i - 1 ] == "Si":

            if arrayAccionesLeon[ i - 1 ] == "Avanzando\n" or arrayAccionesLeon[ i - 1 ] == "Avanzando":

                if int(arrayDistanciaEntreAmbos[ i - 1 ]) >= 3:
                    vecesHuirPorAvanzarEnMira += 1

        if arrayLeonEnLamira[ i - 1 ] == "No\n" or arrayLeonEnLamira[ i - 1 ] == "No":

            if arrayAccionesLeon[ i - 1 ] == "Avanzando\n" or arrayAccionesLeon[ i - 1 ] == "Avanzando":

                if int(arrayDistanciaEntreAmbos[ i - 1 ]) >= 3:
                    vecesHuirPorAvanzarFueraDeMira += 1
      
    #print("\nVeces que huyó por avanzar en mira: ",vecesHuirPorAvanzarEnMira)
    #print("\nVeces que huyó por avanzar Fuera de mira: ",vecesHuirPorAvanzarFueraDeMira,"\n")
    

    probabilidadHuirPorAvanzarEnMira = vecesHuirPorAvanzarEnMira / vecesQueHuyoEImpala
    probabilidadHuirPorAvanzarFueraDeMira = vecesHuirPorAvanzarFueraDeMira / vecesQueHuyoEImpala

    #print("\nProbabilidad de que huya por avanzar en mira: ",probabilidadHuirPorAvanzarEnMira)
    #print("\nProbabilidad de que huya por avanzar Fuera de mira: ",probabilidadHuirPorAvanzarFueraDeMira,"\n")
    


    #  *****************************************************************************************
    #¿Cuál es la probabilidad que huya dado que el león se escondió?
    for i in posicionesParaVerificar:

        if arrayLeonEnLamira[ i - 1 ] == "Si\n" or arrayLeonEnLamira[ i - 1 ] == "Si":

            if arrayAccionesLeon[ i - 1 ] == "Escondido\n" or arrayAccionesLeon[ i - 1 ] == "Escondido":
                vecesHuirPorEsconderseEnMira += 1

        if arrayLeonEnLamira[ i - 1 ] == "No\n" or arrayLeonEnLamira[ i - 1 ] == "No":

            if arrayAccionesLeon[ i - 1 ] == "Escondido\n" or arrayAccionesLeon[ i - 1 ] == "Escondido":
                vecesHuirPorEsconderseFueraDeMira += 1
    
    #print("\nVeces que huyó por esconderse en mira: ",vecesHuirPorEsconderseEnMira)
    #print("\nVeces que huyó por esconderse fuera de mira: ",vecesHuirPorEsconderseFueraDeMira,"\n")


    probabilidadHuirPorEsconderseEnMira = vecesHuirPorEsconderseEnMira / vecesQueHuyoEImpala
    probabilidadHuirPorEsconderseFueraDeMira = vecesHuirPorEsconderseFueraDeMira / vecesQueHuyoEImpala

    #print("\nProbabilidad de que huya por esconderse en mira: ",probabilidadHuirPorEsconderseEnMira)
    #print("\nProbabilidad de que huya por esconderse Fuera de mira: ",probabilidadHuirPorEsconderseFueraDeMira,"\n")





    #  *****************************************************************************************
    #¿Cuál es la probabilidad que huya dado que el león atacó?
    for i in posicionesParaVerificar:

        if arrayLeonEnLamira[ i - 1 ] == "Si\n" or arrayLeonEnLamira[ i - 1 ] == "Si":

            if arrayAccionesLeon[ i - 1 ] == "Atacando\n" or arrayAccionesLeon[ i - 1 ] == "Atacando":

                if int(arrayDistanciaEntreAmbos[ i - 1 ]) >= 3:
                    vecesHuirPorAtacarEnMira += 1

        if arrayLeonEnLamira[ i - 1 ] == "No\n" or arrayLeonEnLamira[ i - 1 ] == "No":

            if arrayAccionesLeon[ i - 1 ] == "Atacando\n" or arrayAccionesLeon[ i - 1 ] == "Atacando":

                if int(arrayDistanciaEntreAmbos[ i - 1 ]) >= 3:
                    vecesHuirPorAtacarFueraDeMira += 1


    #print("\nVeces que huyó por atacar en mira: ",vecesHuirPorAtacarEnMira)
    #print("\nVeces que huyó por atacar fuera de mira: ",vecesHuirPorAtacarFueraDeMira,"\n")

    probabilidadHuirPorAtacarEnMira = vecesHuirPorAtacarEnMira / vecesQueHuyoEImpala
    probabilidadHuirPorAtacarFueraDeMira = vecesHuirPorAtacarFueraDeMira / vecesQueHuyoEImpala

    #print("\nProbabilidad de que huya por atacar en mira: ",probabilidadHuirPorAtacarEnMira)
    #print("\nProbabilidad de que huya por atacar fuera de mira: ",probabilidadHuirPorAtacarFueraDeMira,"\n")


    #ASIGANMOS LAS PROBABILIDADES A LOS ATRIBUTOS DEL LEÓN

    myLeon.PAvanzarEnMira = probabilidadHuirPorAvanzarEnMira
    myLeon.PAvanzarFueraDeMira = probabilidadHuirPorAvanzarFueraDeMira

    myLeon.PEsconderseEnMira = probabilidadHuirPorEsconderseEnMira
    myLeon.PEsconderseFueraDeMira = probabilidadHuirPorEsconderseFueraDeMira

    myLeon.PAtacarEnMira = probabilidadHuirPorAtacarEnMira
    myLeon.PAtacarFueraDeMira = probabilidadHuirPorAtacarFueraDeMira


     #saber en que posiciones murió el Impala
    j = 1
    for i in arrayAccionImpala:
        if i == "Muerto" or i == "Muerto\n":
            vecesQueMurio.append(j)
        j +=1
    

    #print("Veces que murió: ",vecesQueMurio,"\n")
    #PAtaqueExitosoEnLaPosicion contadorPorPosicion

    for i in vecesQueMurio:

        if ( arrayDistanciaEntreAmbos[i - 1] == "9" or arrayDistanciaEntreAmbos[i - 1] == "9\n" ) :
           contadorPorPosicion[7] += 1

        if ( arrayDistanciaEntreAmbos[i - 1] == "8" or arrayDistanciaEntreAmbos[i - 1] == "8\n" ) :
           contadorPorPosicion[6] += 1

        if ( arrayDistanciaEntreAmbos[i - 1] == "7" or arrayDistanciaEntreAmbos[i - 1] == "7\n" ) :
           contadorPorPosicion[5] += 1
        
        if ( arrayDistanciaEntreAmbos[i - i] == "6" or arrayDistanciaEntreAmbos[i - 1] == "6\n" ) :
           contadorPorPosicion[4] += 1
        
        if ( arrayDistanciaEntreAmbos[i - 1] == "5" or arrayDistanciaEntreAmbos[i - 1] == "5\n" ) :
           contadorPorPosicion[3] += 1
        
        if ( arrayDistanciaEntreAmbos[i - 1] == "4" or arrayDistanciaEntreAmbos[i - 1] == "4\n" ) :
           contadorPorPosicion[2] += 1
        
        if ( arrayDistanciaEntreAmbos[i - 1] == "3" or arrayDistanciaEntreAmbos[i - 1] == "3\n" ) :
           contadorPorPosicion[1] += 1

        if ( arrayDistanciaEntreAmbos[i - 1] == "2" or arrayDistanciaEntreAmbos[i - 1] == "2\n" ) :
           contadorPorPosicion[0] += 1


    i = 0
    while i < 8:
        
        PAtaqueExitosoEnLaPosicion[i] = contadorPorPosicion[i] / len(vecesQueMurio)
        
        i += 1


    #Le pasamos los datos calculados al león
    j = 0
    for i in PAtaqueExitosoEnLaPosicion:
        myLeon.PAtacarDependiendoLaPosicion[j] = i

        j += 1


    print("\n\n\n")



def leonEnLaMira():
    #Llenamos los arrays de datos
    llenarArraysGlobales()

    #Verificamos que los arrays contengan datos
    if len(arrayAccionesLeon) != 0 and len(arrayReaccionImpala) != 0 and len(arrayLeonEnLamira) != 0:
        CalcularProbabilidades()



#Verifica si el Impala está viendo o no al león
def verificarEstadoImpala():

    myLeon.zonasPeligrosas.clear()
    if myImpala.estado == "Viendo a la izquierda":

        myLeon.zonasPeligrosas.append(6)
        myLeon.zonasPeligrosas.append(7)
        myLeon.zonasPeligrosas.append(8)

    if myImpala.estado == "Viendo a la derecha":

        myLeon.zonasPeligrosas.append(2)
        myLeon.zonasPeligrosas.append(3)
        myLeon.zonasPeligrosas.append(4)

    if myImpala.estado == "Viendo al frente":

        myLeon.zonasPeligrosas.append(1)
        myLeon.zonasPeligrosas.append(2)
        myLeon.zonasPeligrosas.append(8)

    if myImpala.estado == "Bebiendo agua":

        myLeon.zonasPeligrosas.clear
        myLeon.zonasPeligrosas.append(4)
        myLeon.zonasPeligrosas.append(5)
        myLeon.zonasPeligrosas.append(6)

    #if myImpala.estado == "Está huyendo":



#Aquí el león tomará la desición de qué acción realizará
def accionesLeon():

    acccionParaRealizarLeon = 0

    """Es importante antes que nada verificar en qué estado está el impala, una vez que lo hayamos verificado
    tendremos las zonas peligrosas y en base a llo el león debera tomar al decisión si avanzar,  esconderse
    o atacar"""
    verificarEstadoImpala()

    #print("Ya en accionesLeon() despues de verificar estado impala la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)


    """Verificar con búqueda binaria que el león no se encuentre en una zona de peligro, recordar que solo avanza en linea recta
        si se encunetra en la zona de peligro y no está escondido entonces en Impala huíra.
        hay que gradar cada uno de esos casos y habra que sacar probabilidades con respecto de todas los alementos que tenemos en lso archivos
        para ver que elecciones va a tomar el león."""  

    #En este caso el león NO SE ENCUENTRA EN UNA ZONA DE PELIGRO
    if busqieda_binaria(myLeon.zonasPeligrosas, myLeon.posicionInicial, 0, len( myLeon.zonasPeligrosas ) - 1) == -1:

        myLeon.zonaSegura = True

    #AQUÍ SÍ SE ENCUENTRA EN UNA ZONA DE PELIGRO
    else:

        myLeon.zonaSegura = False

    #En esta función se calculan las probabilidades
    #leonEnLaMira()

    #print("Ya en accionesLeon() despues de verificar zona segura la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)

    #Esto sirve para el entrenamiento
    if myProcesoActual.tipoDeEjecución == "Entrenamiento":

        accionAlAzar = random.randint(1,3)

        if accionAlAzar == 1:
            myLeon.avanzar()

        if accionAlAzar == 2:
            myLeon.esconderse()

        if accionAlAzar == 3:
            myLeon.atacar()

        return 10

    

    #Se calculan las probabilidades
    CalcularProbabilidades()

    #print("Ya en accionesLeon() despues de calcular probabilidades  la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)

    #Fuera de la mira del impala
    if myLeon.zonaSegura == True:

        if myLeon.PAvanzarFueraDeMira == myLeon.PEsconderseFueraDeMira:

            #Seleccionamos la mejor probabilidad que puede tomar el León
            acccionParaRealizarLeon = min( myLeon.PAvanzarFueraDeMira, myLeon.PAtacarFueraDeMira )

        else:

            #Seleccionamos la mejor probabilidad que puede tomar el León
            acccionParaRealizarLeon = min( myLeon.PAvanzarFueraDeMira, myLeon.PEsconderseFueraDeMira, myLeon.PAtacarFueraDeMira )

        #Deacuerdo a la probabilidad el león elige una acción para realizar
        if acccionParaRealizarLeon == myLeon.PAvanzarFueraDeMira:

            myLeon.avanzar()

        if acccionParaRealizarLeon == myLeon.PAtacarFueraDeMira:

            myLeon.atacar()
            
        #print("Ya en accionesLeon() despues de zona segura true  la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)

    #En el rango de visión del impala
    else:

        #print("Ya en accionesLeon() entrando a  zona segura false  la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)
        #Seleccionamos la mejor probabilidad que puede tomar el León
        acccionParaRealizarLeon = min( myLeon.PAvanzarEnMira, myLeon.PEsconderseEnMira, myLeon.PAtacarEnMira )


        #Deacuerdo a la probabilidad el león elige una acción para realizar
        if acccionParaRealizarLeon == myLeon.PAvanzarEnMira:

            myLeon.avanzar()

        if acccionParaRealizarLeon == myLeon.PEsconderseEnMira:
            
            myLeon.esconderse()

        if acccionParaRealizarLeon == myLeon.PAtacarEnMira:
            
            myLeon.atacar()

        #print("Ya en accionesLeon() despues de zona segura false  la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)





#Elige una accion al azar del Impala
def accionImpala():

    #La única condición en dónde el impala puede morir
    if  myLeon.PAtacarDependiendoLaPosicion[ (9-myLeon.distanciaRecorrida) - 2 ]  > 0 or ( 9-myLeon.distanciaRecorrida == 2 and myLeon.estado == "Atacando"):
        myImpala.estado = "Muerto"

        return 0



    #verificar si está viendo al león para que huya
    if ( myLeon.zonaSegura == False and myLeon.estado == "Avanzando" ) or ( 9 - myLeon.distanciaRecorrida < 3) or (myLeon.estado == "Atacando"):
        myImpala.huir()

    else:
        accionAleatoria = random.randint(1,4)

        if accionAleatoria == 1:
            myImpala.verIzquierda()
    
        if accionAleatoria == 2:
            myImpala.verDerecha()

        if accionAleatoria == 3:
            myImpala.verFrente()

        if accionAleatoria == 4:
            myImpala.beberAgua()



def transcursoEventos( contador, numeroDeReinicio ):

    exito = 1
    vecesEjecutadaEstaFuncion = 0

    #Imprimir estado inicial 
    if contador == 1:
        print("\n")
        print("--------------------INICIO EVENTO INICIAL----------------------------")
        print("Posición inicial Leon: ",myLeon.posicionInicial)
        print("Estado Impala: ",myImpala.estado)
        print("Estado leon: ",myLeon.estado)
        print("Distancia entre ambos: ",9 - myLeon.distanciaRecorrida," bloques")
        print("--------------------FIN EVENTO INICIAL-------------------------------")
        print("\n")

    #El impala realiza una accion al azar o huye del león
    accionImpala()
    
    
    #El león realizar una accion 
    if myImpala.estado == "Muerto":
        myLeon.estado = "Comiendo Impala"
    else:
        #print("Antes de entrar a accionesLeon() la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)
        accionesLeon()
    #print("Después de sali de accionesLeon() la distancia entre ambos es: ", 9 - myLeon.distanciaRecorrida)


    if myImpala.estado == "Muerto":

        print("\n\n")
        print("--------------------INICIO EVENTO ",contador,"----------------------------")
        print("Posición inicial Leon: ",myLeon.posicionInicial)
        print("Estado Impala: ","Huyendo")
        print("Estado leon: ","Atacando")
        print("Distancia entre ambos: ",0 ," bloques")
        print("--------------------FIN EVENTO ",contador,"-------------------------------")
        print("\n")


    if myImpala.estado == "Muerto":
        contador += 1

    print("\n")
    print("--------------------INICIO EVENTO ",contador,"---------------------------")
    print("Posición inicial Leon: ",myLeon.posicionInicial)
    print("Estado Impala: ",myImpala.estado)
    print("Estado leon: ",myLeon.estado)

    if myImpala.estado == "Muerto":
        print("Distancia entre ambos: ","0"," bloques")
    else:
        print("Distancia entre ambos: ",9 - myLeon.distanciaRecorrida ," bloques")

    print("--------------------FIN EVENTO ",contador,"------------------------------")
    print("\n")


    #Guardamos lo datos de esta iteración en los archivos

    #Ver si hay datos en el archivo
    llenarArraysGlobales()

    archivoTexto = open("AccionesLeon.txt","a")
    if len(arrayAccionesLeon) == 0:
        archivoTexto.write(myLeon.estado)
    else:
        archivoTexto.write("\n" + myLeon.estado)

    archivoTexto.close()


    archivoTexto2 = open("AccionesImpala.txt","a")
    if len(arrayAccionImpala) == 0:
        archivoTexto2.write(myImpala.estado)
    else:
        archivoTexto2.write("\n" + myImpala.estado)

    archivoTexto2.close()


    archivoTexto3 = open("LeonEnLaMira.txt","a")
    if len(arrayLeonEnLamira) == 0:
        if myLeon.zonaSegura == True:

            archivoTexto3.write("No")
        else:
            archivoTexto3.write("Si")
    else:
        if myLeon.zonaSegura == True:

            archivoTexto3.write("\nNo")
        else:
            archivoTexto3.write("\nSi")

    archivoTexto3.close()



    archivoTexto4 = open("DistanciEntreAmbos.txt","a")
    if len(arrayDistanciaEntreAmbos) == 0:

        archivoTexto4.write( str(9 - myLeon.distanciaRecorrida) )
 
    else:
        
        archivoTexto4.write( "\n" + str(9 - myLeon.distanciaRecorrida) )

    archivoTexto4.close()



    #Reiniciar el entrenamiento ya que el Impala huyó
    if myImpala.estado == "Huyendo":

        print("\nEl impala huyó ya que detectó al león. Vamos a reiniciar el experimiento.")
        
        restablecerValores()

        return 1

    if myImpala.estado == "Muerto":
        return 0


   
def Entrenamiento_Atacar():

    #J representa la distancia que hay entre ambos
    j = 9
    while j >= 1:
        accionImpala()
        myLeon.atacar()

        #La única condición en dónde el impala puede morir
        if  j == 2 and myLeon.estado == "Atacando":
            myImpala.estado = "Muerto"

        #Guardamos lo datos de esta iteración en los archivos

        #Ver si hay datos en el archivo
        llenarArraysGlobales()

        archivoTexto = open("AccionesLeon.txt","a")
        if len(arrayAccionesLeon) == 0:
            archivoTexto.write(myLeon.estado)
        else:
            archivoTexto.write("\n" + myLeon.estado)

        archivoTexto.close()


        archivoTexto2 = open("AccionesImpala.txt","a")
        if len(arrayAccionImpala) == 0:
            archivoTexto2.write(myImpala.estado)
        else:
            archivoTexto2.write("\n" + myImpala.estado)

        archivoTexto2.close()


        archivoTexto3 = open("LeonEnLaMira.txt","a")
        if len(arrayLeonEnLamira) == 0:
            if myLeon.zonaSegura == True:

                archivoTexto3.write("NoDefinido")
            else:
                archivoTexto3.write("NoDefinido")
        else:
            if myLeon.zonaSegura == True:

                archivoTexto3.write("\nNoDefinido")
            else:
                archivoTexto3.write("\nNoDefinido")

        archivoTexto3.close()



        archivoTexto4 = open("DistanciEntreAmbos.txt","a")
        if len(arrayDistanciaEntreAmbos) == 0:

            archivoTexto4.write( str(j) )
 
        else:
        
            archivoTexto4.write( "\n" + str(j) )

        archivoTexto4.close()
        


        j -= 1

    restablecerValores()



#En esta función quiero que sea la representación de cada momento T en el mundo virtual
def Iniciar( numeroDeEventos ):

    #creamos los archivos
    archivoTexto = open("AccionesLeon.txt","a")
    archivoTexto.close()

    archivoTexto2 = open("AccionesImpala.txt","a")
    archivoTexto2.close()

    archivoTexto3 = open("LeonEnLaMira.txt","a")
    archivoTexto3.close()

    archivoTexto3 = open("DistanciEntreAmbos.txt","a")
    archivoTexto3.close()

    myProcesoActual.archivosCreados = True

    #si es 0 entonces el león cazó al impla, si es 1 entonces el impala huyo
    resultado = 6

    numeroDeReinicio = 0

    i = 1
    while i <= numeroDeEventos:
        resultado = transcursoEventos( i, numeroDeReinicio ) 

      
        #Terminar la ejecución porque ya se cazó al impala
        if resultado == 0:
            i = numeroDeEventos + 1


        if myProcesoActual.tipoDeEjecución != "Entrenamiento":
            time.sleep(1)


        i += 1




def portada():

    opcion = 0

    print("| PROYECTO FINAL SISTEMAS INTELIGENTES |")
    print("\n\nINTEGRANTES DEL EQUIPO")
    print("\n- CRUZ DOMÍNGUEZ ALAN ALBERTO")
    print("\n- HERNÁNDEZ SANTANA XIMENA")
    print("\n- ")
    print("\n- OCAÑA AMEZCUA CHRISTOPHER")
    print("\n- SENTIES PEÑA EMILIO EFRAÍN\n")

    #print("\n\nPresiona 1 para continuar")

    os.system("pause")
    
    os.system("cls")





def MenuPrincipal():

    opcion = 0
    numeroDeEventos = 100

    restablecerValores()

    print("| PROYECTO FINAL SISTEMAS INTELIGENTES |")

    print("\n¿Qué deseas realizar?")

    print("\n1.- Entrenar al león")
    print("\n2.- Ir de cacería")
    print("\n3.- Salir\n")

    opcion = int(input( "Opcion: " ))

    while opcion < 1 or opcion > 3:
        os.system("cls")
        print("| PROYECTO FINAL SISTEMAS INTELIGENTES |")

        print("\n¿Qué deseas realizar?")

        print("\n1.- Entrenar al león")
        print("\n2.- Ir de cacería")
        print("\n3.- Salir\n")

        opcion = int(input( "Opcion: " ))

    os.system("cls")

    if opcion == 1:
    
        print("| ENTRENAMIENTO |\n\n")
        numeroDeEventos = int( input( "¿Cuántos ciclos de entrenimento deseas?\n\nCiclos: " ) )

        myProcesoActual.tipoDeEjecución = "Entrenamiento"
    
        Iniciar( numeroDeEventos )

        i = 0
        while i < 5:
            Entrenamiento_Atacar()
            i += 1

        print("\n\nTerminando entrenamiento ...\n\n")
        time.sleep(1)

        os.system("cls")
        os.system("pause")
        repetirPrograma()



    if opcion == 2:

        print("\n| CACERÍA |\n\n\n")


        #Aquí vamos a verificar que haya datos en los archivos, si no hay entonces no dejaremos que prosiga la ejecución de este
        #fragmento de código

        try:
            llenarArraysGlobales()
        except:
            myProcesoActual.archivosCreados = False

       
        if myProcesoActual.archivosCreados == False: 

            print("\nPOR FAVOR, PRIMERO ENTRENA AL LEÓN, ES FUNDAMENTAL EL ENTRENAMIENTO PARA LA EJECUCIÓN DEL PROGRAMA.\n")
            os.system("pause")
            os.system("cls")
            print("\n| CACERÍA |\n")
            repetirPrograma()

        else:
            
            myProcesoActual.tipoDeEjecución = "Cacería"

            posicionInicialLeon = int( input( "¿En cuál de las 8 posiciones deseas que iniciel el león?\n\nPosición: " ) )

            while posicionInicialLeon < 1 or posicionInicialLeon > 8:
                print("Las únicas posiciones disponible sson: 1, 2, 3, 4, 5, 6, 7 y 8. Por favor elije una posición válida.")

                os.system("cls")

                print("| CACERÍA |\n\n\n")

                myProcesoActual.tipoDeEjecución = "Cacería"

                posicionInicialLeon = int( input( "¿En cuál de las 8 posiciones deseas que iniciel el león?\n\nPosición: " ) )

            myLeon.posicionInicial = posicionInicialLeon
    
            Iniciar( numeroDeEventos )

            os.system("pause")
            repetirPrograma()

    if opcion == 3:
        print("\nTerminando programa, hasta luego.\n")
        return

        



def repetirPrograma():

    print("\n\n\n¿Quieres regresar al menú principal?")

    print("\n\n1.-Sí")
    print("2.-No\n")

    opcion =  int( input( "Opción: " ) ) 

    while opcion < 1 or opcion > 2:
        os.system("cls")

        print("¿Quieres regresar al menú principal?")

        print("\n\n1.- Sí")
        print("\n2.- No")

        opcion =  int( input( "Opción: " ) )



    if opcion == 1:
        os.system("cls")
        MenuPrincipal()
    else:

        print("\nTerminando programa. Hasta luego.\n")
        return


portada()
MenuPrincipal()
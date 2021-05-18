#!/usr/bin/python3
'''
Equipo: Draco
Integrantes: Humberto Alessandro Torres López
             Kevin Sebastian Guerrero Rivera
             Luis Gregorio

Fecha: 27/03/2020

Modo de uso:
--------------------------------------------------
Ingrese el siguinte comando para usar el programa:

Desde Windows CMD:

pares.py -m # cartas a tomar-j (jugador1) -j (jugador2)
-m no es obligatorio y tiene por default 5***

Ejemplo:

pares.py -m 5 -j ale -j kevin -j luis 

Para que funcione correctamente:
- Se necesita un minimo de 2 jugadores
- Que al multiplicar el numero de jugadores(-j) por (-m) el resultado sea <= 52
'''

import argparse
import tarjetas

def game_generator(jugador, mano, Deck):

    for j in jugador: #Recorre jugadores
        name = j #Le asigna nombre al jugador en la posicion j
        j = tarjetas.Player(name) #Ahora se lo da en la clase Player al atributo name
        Deck.hand_generator(j,mano) #Llama a la funcion para generar mano y le pasa el nombre del jugador y la cantidad de cartas para su mano
        j.crea_dict() #Crea otro diccionario con las manos actuales
    hand_generator(Deck) #Manda a llamar la impresion de la mano de los jugadores
    

def hand_generator(Deck): #Nos sirve para desplegar las manos de ambos jugadores

    player_list=Deck.player_list #Esta lista sirve para utilizar la lista de jugadores
    
    for j in player_list:
        print()
        print(j.name) #Imprime el nombre del jugador en posicion j?, el punto name no estoy muy seguro porque es necesario
        print("----------")
        j.showHand() #Muestra la mano del jugador en posicion j?
        print()

def score_calculator(player_list,Deck): #Calcula el puntaje de cada jugador proporcionado por la lista
    
    for jugador in player_list: #Recorre los jugadores
        card_values = [x.values for x in jugador.hand]#Extrae los valores de las cartas en la mano
        for values in card_values: #Recorre todos los valores en card_values
            if card_values.count(values) >= 2: #if el valor que esta contenido es mayor o igual a 2
                #La puntuacion del jugador se acumulara y sera igual a el valor contenido en card_values
                jugador.puntuacion += card_values.count(values)
                #Si el valor de la carta difiere de los demas pues se sigue recorriendo.
                card_values = [x for x in card_values if x!= values]
        show_score(jugador)


def winner(player_list):  #Calcula el jugador winner de lista de jugadores dada
    
    #puntajes es una lista de las puntuaciones hechas al recorrer el numero de jugadores
    #EJ. Ale: 42 pts Kevin: 22pts Paredes: 10pts
    puntajes = [x.puntuacion for x in player_list]
    
    puntaje_winner = max(puntajes) #La funcion max, nos dara al winner que tenga el maximo puntaje, en este caso ALE

    if puntaje_winner == 0: #El print describe esta situacion
        print("En ninguna jugada hubo pares o tercias. EMPATE")
        
    #si el puntaje winner es mayor que 1 y diferente de 0
    elif (puntajes.count(puntaje_winner) > 1) and puntaje_winner != 0:

        #Lista es igual a recorrido en lista de jugadores si puntuacion es igual a puntaje winner, desplegar el nombre del ganador
        lista = [ j for j in player_list if (j.puntuacion == puntaje_winner)]
        tie_breaker(lista) 
        
    #Si el puntaje winner es igual a 1
    elif puntajes.count(puntaje_winner) == 1:
        
        Player = player_list[puntajes.index(puntaje_winner)]
        show_winner(Player)

def tie_breaker(player_list):
    ''' Calcula al jugador que uso mas cartas en la jugada para
        declararlo winner en el caso de que exista un empate
        de puntos
    '''
    lista_len = [] #Lista
    
    for j in player_list: #recorre lista de jugadores

        len_cartas = 0 #Largo de cartas inicia en 0
        card_values = [x.values for x in j.hand] #Extrae el valor de las cartas en la mano

        for values in card_values: #Recorre la lista de valores de las cartas
            if card_values.count(values) >= 2: #Si incluye valores mayores o igual a 0
                len_cartas += 1 #Valor de cant.cartas se incrementa en 1
                
        lista_len.append(len_cartas)#Se le suma el largo de cartas Al largo de la lista 
        
    winner = max(lista_len) #El winner sera el que tenga el maximo de lista
    Player = player_list[lista_len.index(winner)]
    show_winner(Player) #Despliega al winner

def show_score(Player):
    #Despliega la puntuacion del jugador
    print("El puntaje de {nombre} es: {puntos}".format(nombre = Player.name, puntos = Player.puntuacion))

def show_winner(Player): #Despliega el nombre y puntuacion del jugador winner

    print("Ganador: {nombre} con {puntos} puntos".format(nombre = Player.name, puntos = Player.puntuacion))
    show_plays(Player)

def show_plays(Player): #Despliega la cantidad de pares y tercias que obtuvo el jugador
    
    dicc = dict()
    dicc = Player.dict_play #Se le asigna el diccionario de la jugada a dicc

    pares   = len(dicc["pares"])
    tercias = len(dicc["tercias"])

    print("Gano con",pares,"par(es) y",tercias,"tercia(s)")

    
def main(mano, jugador):
    if ((len(jugador)*mano) > 52) and (len(jugador) >= 2):
        print("No hay suficientes cartas para este juego")
    else:
        Deck=tarjetas.Deck()
        player_list=Deck.player_list
        
        game_generator(jugador,mano,Deck) #DESPLIEGA MANOS
        score_calculator(player_list, Deck) #CALCULA PUNTAJES
        winner(player_list) #MUESTRA AL GANADOR
       
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mano',dest='mano',help="numero de cartas a repartir en cada mano",required=True,default=5,type=int)
    parser.add_argument('-j','--jugador',dest='jugador',help="nombre del jugador",action="append",required=True)
    args    = parser.parse_args()
    mano  = args.mano
    jugador  = args.jugador
    main(mano, jugador)

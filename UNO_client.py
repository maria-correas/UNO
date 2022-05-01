#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EL UNO VERSIÓN RÁPIDA
"""
#from random import random
#import numpy as np


from multiprocessing.connection import Client
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys
jugadores = 3
 
colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
         

#clase carta
class Carta():
    
    def __init__(self, valor, color):
        self.valor = valor
        self.color = color
    
    def __str__ (self):
        return f"{self.valor} {self.color}"


#mazo que contiene todas las cartas
class Mazo():
    
    def __init__(self): 
        import random
        self.cartas =[]
        for color in colores:
            for valor in valores:
                self.cartas.append(Carta(valor,color))    
            self.cartas.append(Carta("Cambio de color","Neutro"))   
        random.shuffle(self.cartas) #esto es para barajar las cartas
        
      
    def __str__(self):
        for carta in self.cartas:
            str(carta)
    
    def robar(self):
        carta = self.cartas.pop(0)
        return carta

#clase tablero 
class Tablero():
    def __init__(self):

        #self.carta = {"carta": Carta(random.choice(valores),random.choice(colores))}
        self.carta = {"carta": mazo.robar()}
        self.players = [Player(i) for i in range(3)]
        self.contador= [7,7,7]
        self.running = True
        self.mazo = mazo

   
    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
        
    def __str__(self):
        return str(self.carta["carta"])
    
    def update(self, gameinfo):
        self.carta["carta"] = inverso_carta(gameinfo['carta_mesa'])
        self.contador = inverso_contador(gameinfo['contador'])
        self.running = gameinfo['is_running']
        for i in range (3):
            self.players[i]= inverso_player(separa_players(gameinfo['players'])[i])

        


    
def inverso_carta(info):
    lista=info.split(",")
    valor = lista[0]
    color = lista[1]
    carta = Carta(valor,color)
    return str(carta)  

def inverso_contador(info):
    lista=info.split(",")
    l2 = []
    for e in lista:
        en = int(e)
        l2.append(en)
    return l2
        


def separa_players(info):
    lista_players = info.split(";")
    return lista_players
    
def inverso_player(info):
    lista=info.split(",")
    idd = int(lista.pop(0))
    
    mano=[]
    for i in range(0, len(lista)-1,2):
        valor = lista[i]
        color = lista[i+1]
        carta = Carta(valor,color)
        mano.append(str(carta))
    
    return idd, mano
    
    
        
    
    
    
#clase jugador 
class Player():
    def __init__(self, idd):
        self.idd = idd 
        self.mano = [mazo.robar() for i in range(7)] #roba cartas del mazo ya aleatorizado
    
    def __str__ (self):
        lista=[]
        for carta in self.mano:
            lista.append(str(carta))
        return str(lista)
            
        
        #return f"Jugador {self.nombre} tiene {self.mano}"
  

mazo = Mazo() 

def main(ip_address):

    try:
        with Client((ip_address, port), authkey=b'secret password') as conn:
           
            idd = conn.recv() #,gameinfo
            print(f"Soy el jugador {idd}")
            gameinfo = conn.recv()
            #print(gameinfo) 
            tablero = Tablero()
            tablero.update(gameinfo)
            print('nuestra mano es '+ str(tablero.players[idd]))
            print("La carta central es: " + str(tablero.carta))
            #display = Display(game)
            while tablero.is_running():
                events = input('¿Qué quieres hacer ahora? ') #display.analyze_events(side)
                #for ev in events:
                conn.send(events)
                if events == 'quit':
                    tablero.stop()
                recibido = conn.recv()
                print(recibido)
                
                
                gameinfo = conn.recv()
                tablero.update(gameinfo)
                print('nuestra mano es '+ str(tablero.players[idd]))
                print("El número de cartas de los jugadores es: " + str(tablero.contador))
                print("La carta central es: " + str(tablero.carta))
                print("")
                print("")
                #display.refresh()
                #display.tick()
    except:
        traceback.print_exc()
    #finally:
     #   pygame.quit() #duda como cerrarlo


if __name__=="__main__":
    ip_address = "127.0.0.1"
    port= 6000
    if len(sys.argv)==2:
        ip_address = sys.argv[1]
    elif len(sys.argv)>2:
        ip_address = sys.argv[1]
        port = int(sys.argv[2])
    main(ip_address)

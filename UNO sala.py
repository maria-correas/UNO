#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 18:49:39 2022

@author: mat
"""

from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys

"""
EL UNO VERSIÓN RÁPIDA
"""
#from random import random
#import numpy as np

jugadores = 2

colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
    
        

#clase carta
class Carta():
    
    colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
    valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
    
    def __init__(self, valor, color):
        self.valor = valor
        self.color = color
    
    def __str__ (self):
        return f"{self.valor},{self.color}"
    

#mazo que contiene todas las cartas
class Mazo(Carta):
    
    def __init__(self):
        self.cartas =[]
        for color in self.colores:
            for valor in self.valores:
                self.cartas.append(Carta(valor,color))
                
            self.cartas.append(Carta("Cambio de color","Neutro"))   
    def muestraCarta(self): #muestra la ultima carta 
        return f" {self.cartas[-1].valor} {self.cartas[-1].color}"

         
    def __str__2 (self):
        for carta in self.cartas:
            carta.__str__()


#clase tablero 
class Tablero(Carta):
    def __init__(self,manager):
        import random  #Como conseguir que carta sea compartida
        self.carta = manager.Carta(random.choice(self.valores),random.choice(self.colores))
        self.players = manager.list([Player(i) for i in range(3)])
        self.contador= manager.list([7,7,7])
        self.running = Value('i',1)
        self.lock = Lock()

    
    def get_player(self, side):
        return self.players[side]

    def get_carta(self):
        return self.carta
    def change_carta(self,cartita):
        self.lock.acquire()
        self.carta = cartita
        self.lock.release()
        
    def change_contador(self):
        self.lock.acquire()
        for i in range(3):
            self.contador[i] = len(self.players[i].mano)
    
        self.lock.release()

    def get_contador(self):
        return self.contador

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.lock.acquire()
        self.running.value = 0
        self.lock.release()
        
    def puede_echar(self, carta):
        return ((carta.valor == self.carta.valor) or
                (carta.color == self.carta.color)) or (carta.valor == 'Cambio de color')


        
    def get_info(self):
        info = {
            
            'carta_mesa': self.carta.get_carta(),
            'contador': list(self.contador),
            'is_running': self.running.value == 1
        }
        return info

        
    def __str__(self):
        return self.carta.muestra_carta()
       


    


#clase jugador 
class Player():
    
    def __init__(self, idd, nombre):
        import random
        self.nombre = nombre 
        self.mano = [random.choice(mazo.cartas) for i in range(7)]
    
    def __str__ (self):
        for carta in self.mano:
            print(carta.__str__())
        #return f"Jugador {self.nombre} tiene {self.mano}"
    
    
    def robar(self, numero, cartas):
        import random
        
        for i in range (numero):
            carta = random.choice(cartas)
            self.mano.append(carta)
          
            
    def puede_echar(self, carta, tablero):
        return ((carta.valor == tablero.carta.valor) or (carta.color == tablero.carta.color))


    def echar_carta (self, tablero):
        seguir = True
        contador = 0
        while seguir != False and contador < len(self.mano):
            if self.puede_echar(self.mano[contador], tablero):
                print("Puede echar esta carta")
                print(self.mano[contador].__str__())
                print("_________")
                tablero.carta = self.mano[contador] #modificamos el tablero 
                self.mano.pop(contador)
                seguir = False
            contador += 1
   
mazo = Mazo() 
         
def player(idd, conn, tablero):
    import random
    try:
        print(f"starting player {idd}:{tablero.get_info()}")
        conn.send( (idd, tablero.get_info()) )
        
        while tablero.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command.isdigit():
                    cartita = tablero.players[idd].mano[int(command)]
                    if tablero.puede_echar(cartita):
                        if cartita.valor == 'Bloqueo':
                            lista=[0,1,2]
                            lista.pop(idd)
                            b = random.choice(lista)
                            print(f'player {idd} blocked')
                            tablero.players[b].dormir()
                        elif cartita.valor == '+2':
                            print(f'Oh no!, el jugador {idd} ha sacado un chupate 2, todos a robar')
                            tablero.player[(idd+1)%3].robar(2,mazo.cartas)
                            tablero.player[(idd+2)%3].robar(2,mazo.cartas)
                        elif cartita.valor == 'Cambio de color':
                             cartita.color = random.choice(colores)
                        tablero.change_carta(cartita)
                        tablero.players[idd].mano.pop(int(command))
                        tablero.change_contador()
                            
                elif command == "quit":
                    tablero.stop()

            conn.send(tablero.get_info())
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {tablero}")
            
  
def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6000),
                      authkey=b'secret password') as listener:
            n_player = 0
            players = [None, None,None]
            tablero = Tablero(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                players[n_player] = Process(target=player,
                                            args=(n_player, conn, tablero))
                n_player += 1
                if n_player == 2:
                    players[0].start()
                    players[1].start()
                    players[2].start()
                    n_player = 0
                    players = [None, None,None]
                    tablero = Tablero(manager)

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)
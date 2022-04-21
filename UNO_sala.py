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
class Carta(object):
    
    def __init__(self, valor, color):
        self.valor = valor
        self.color = color
    
    def __repr__ (self):
        return f"{self.valor} {self.color}"
    
    def get_info(self):
        return self.valor+","+self.color
    

#mazo que contiene todas las cartas
class Mazo:
    colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
    valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
 
    def __init__(self):
        self.cartas =[]
        for color in self.colores:
            for valor in self.valores:
                self.cartas.append(Carta(valor,color))
                
            self.cartas.append(Carta("Cambio de color","Neutro"))   
    def muestraCarta(self): #muestra la ultima carta 
        return f"{self.cartas[-1].valor} {self.cartas[-1].color}"

         
    def __str__ (self):
        lista =[]
        for carta in self.cartas:
            lista.append(str(carta))
        return lista


#clase tablero 
class Tablero(object):
    def __init__(self,manager):
        import random  
        colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
        valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
 
        self.carta = manager.dict({"carta": Carta(random.choice(valores),random.choice(colores))})
        self.players = manager.list([Player(i) for i in range(3)]) #duda
        self.contador= manager.list([7,7,7])
        self.running = Value('i',1)
        self.lock = Lock()

    
    def get_player(self, idd):
        return self.players[idd]

    def get_carta(self):
        return self.carta["carta"]
    
    def change_carta(self,cartita):
        self.lock.acquire()
        self.carta["carta"] = cartita
        self.lock.release()
        
    def change_contador(self):
        self.lock.acquire()
        for i in range(3):
            self.contador[i] = len(self.players[i].mano)
    
        self.lock.release()

    def get_contador(self):
        return str(self.contador[0])+","+str(self.contador[1])+","+str(self.contador[2])

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.lock.acquire()
        self.running.value = 0
        self.lock.release()
        
    def puede_echar(self, carta):
        return ((carta.valor == self.carta["carta"].valor) or
                (carta.color == self.carta["carta"].color) or 
                (carta.valor == 'Cambio de color'))


        
    def get_info(self,idd):
        info = {
            'carta_mesa': self.carta["carta"].get_info(),
            'contador': self.get_contador(),
            'is_running': self.running.value == 1,
            'player': self.players[idd].get_info()
        }
        return info

        
    def __repr__(self):
        return str(self.carta["carta"]) + ' ' + str(self.contador)
    
    def change_mano(self, idd, n):
        self.lock.acquire()
        print(f"sala1: {idd} {n} {self.players[idd].mano}")
        p = self.players[idd]
        p.mano.pop(n)
        self.players[idd] = p
        print(f"sala2: {self.players[idd].mano}")
        self.lock.release()
        
   


#clase jugador 
class Player():
    
    def __init__(self, idd):
        import random
        self.idd = idd 
        self.mano = [random.choice(mazo.cartas) for i in range(7)]
    
    def __repr__ (self):
        return str(self.mano)
        
    
    def get_info(self):
        strr=""
        for i in range(len(self.mano)):
            strr += ","+self.mano[i].get_info()
        salida = str(self.idd) + strr
        return salida
        
        
    def robar(self, numero, cartas):
        import random
        
        for i in range (numero):
            carta = random.choice(cartas)
            self.mano.append(carta)
          
            
    def puede_echar(self, carta, tablero):
        return ((carta.valor == tablero.carta["carta"].valor) or 
                (carta.color == tablero.carta["carta"].color) or 
                (carta.valor == 'Cambio de color'))
    
    def dormir(self):
        import random 
        import time 
        time.sleep(random.random()*3)
        
'''
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
'''   
mazo = Mazo() 




def trans(mensaje):
    lista = mensaje.split(",")
    return lista





      
def player(idd, conn, tablero):
    try:
        print(f"starting player {idd}:{tablero.get_info(idd)}")
        conn.send( (idd))#, tablero.get_info()) )
        print("c1", tablero.get_info(idd))
        conn.send(tablero.get_info(idd))
        print(tablero)
        while tablero.is_running() :
            command = ""
            while command != "next":
                command = conn.recv()
                print(f"player:{idd}:{command}:")
                mensaje = trans(command)
                if mensaje[0].isdigit():
                    cartita = tablero.players[idd].mano[int(mensaje[0])]
                    if tablero.puede_echar(cartita):
                        if cartita.valor == 'Bloqueo':
                            bloqueado = int(mensaje[1])
                            print(f'player {bloqueado} blocked')
                            tablero.players[bloqueado].dormir()    
                        elif cartita.valor == '+2':
                            print(f'Oh no!, el jugador {idd} ha sacado un chupate 2, todos a robar')
                            tablero.player[(idd+1)%3].robar(2,mazo.cartas)
                            tablero.player[(idd+2)%3].robar(2,mazo.cartas)
                        elif cartita.valor == 'Cambio de color':
                             cartita.color = mensaje[1]
                             print(f'el jugador {idd} ha cambiado de color al {mensaje[1]}')
                        
                        tablero.change_carta(cartita)
                        tablero.change_mano(idd,int(mensaje[0]))
                        print("Hemos borrado el")
                        tablero.change_contador()
                elif 0 in tablero.contador:
                    j =[i for i in range (0,3) if tablero.contador[i] == 0][0]
                    print(f'El jugador {j} ha ganado pringados')
                elif command == "quit":
                    tablero.stop()
                
                print(tablero)
                

                conn.send(tablero.get_info(idd))
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
                print(f'jugador {n_player} aceptado')
                if n_player == 2:
                    players[0].start()
                    players[1].start()
                    players[2].start()
                    #n_player = 0
                    #players = [None, None,None]
                    #tablero = Tablero(manager)
                n_player += 1

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)

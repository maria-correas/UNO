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
class Mazo(Carta):
    
    def __init__(self):
        colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
        valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
 
        self.cartas =[]
        for color in colores:
            for valor in valores:
                self.cartas.append(Carta(valor,color))
                
            self.cartas.append(Carta("Cambio de color","Neutro"))   
      
    def __str__(self):
        for carta in self.cartas:
            print(carta)


#clase tablero 
class Tablero(Carta):
    def __init__(self):
        import random
        colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
        valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
 
        self.carta = {"carta": Carta(random.choice(valores),random.choice(colores))}
        self.players = [Player(i) for i in range(3)]
        self.contador= [7,7,7]
        self.running = True
    
    def get_player(self, side):
        return self.players[side]

    def get_carta(self):
        return self.carta["carta"]

    def get_contador(self):
        return self.contador

    def set_contador(self, idd):
        self.contador[idd]= len(self.players[idd].mano)
        
    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
        
    def __str__(self):
        return str(self.carta["carta"])

        
    def get_info(self):
        info = {            
            'carta_mesa': self.carta.get_carta(),
            'contador': self.contador,
            'is_running': self.running.value == 1,
            'players': None
        }
        return info

    def update(self, gameinfo):
        self.carta["carta"] = gameinfo['carta_mesa']
        self.contador = gameinfo['contador']
        self.running = gameinfo['is_running']
        self.players = gameinfo['players']
        
   

    


#clase jugador 
class Player():
    def __init__(self, idd):
        import random
        self.idd = idd 
        self.mano = [random.choice(mazo.cartas) for i in range(7)]
    
    def __str__ (self):
        lista=[]
        for carta in self.mano:
            lista.append(str(carta))
        return str(lista)
            
        
        #return f"Jugador {self.nombre} tiene {self.mano}"
    
    
    def robar(self, numero, cartas):
        import random
        
        for i in range (numero):
            carta = random.choice(cartas)
            self.mano.append(carta)
          
            
    def puede_echar(self, carta, tablero):
        return ((carta.valor == tablero.carta["carta"].valor) or (carta.color == tablero.carta["carta"].color))


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
#print(mazo.muestraCarta())

#j1 = Player("Maria")
#print(j1.__str__())

#j1.robar(7,mazo.cartas)
#print(j1.__str__())
     

#tablero = Tablero()
#print("La carta del tablero es:")
#print(tablero.carta.__str__()) #muestra la carta del tablero 

#j1.echar_carta (tablero)
#print(j1.__str__())

#print(tablero.carta.__str__())

"""  
j2 = Player("Marla")
#print(j2.__str__())
j2.robar(7,mazo.cartas)
print(j2.__str__())
"""

def main(ip_address):

    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            tablero = Tablero()
            idd = conn.recv() #,gameinfo
            print(f"I am playing {idd}")
            gameinfo = conn.recv()
            #print(gameinfo)
            tablero.update(gameinfo)
            print(tablero.players[idd])
            #display = Display(game)
            while tablero.is_running():
                events = input('¿Qué quieres hacer ahora?') #display.analyze_events(side)
                #for ev in events:
                conn.send(events)
                if events == 'quit':
                    tablero.stop()
                conn.send("next")
                gameinfo = conn.recv()
                tablero.update(gameinfo)
                print(tablero.players[idd])
                #display.refresh()
                #display.tick()
    except:
        traceback.print_exc()
    #finally:
     #   pygame.quit() #duda como cerrarlo


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)

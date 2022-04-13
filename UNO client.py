#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EL UNO VERSIÓN RÁPIDA
"""
#from random import random
#import numpy as np

jugadores = 2
 
        

#clase carta
class Carta():
    
    colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
    valores = ["0","1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
    
    def __init__(self, valor, color):
        self.valor = valor
        self.color = color
    
    def __str__ (self):
        return f" {self.valor} {self.color}"
    

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

         
    def __str__(self):
        for carta in self.cartas:
            carta.__str__()


#clase tablero 
class Tablero(Carta):
    def __init__(self):
        import random
        self.carta = Carta(random.choice(self.valores),random.choice(self.colores))
        self.players = [Player(i) for i in range(3)]
        self.contador= [7,7,7]
        self.running = True
    
    def get_player(self, side):
        return self.players[side]

    def get_carta(self):
        return self.carta

    def get_contador(self):
        return self.contador

    def set_contador(self, idd):
        self.contador[idd]= len(self.players[idd].mano)
        
    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
        
    def __str__(self):
        return self.carta.muestra_carta()
       
        
    def get_info(self):
        info = {
            
            'carta_mesa': self.carta.get_carta(),
            'contador': list(self.contador),
            'is_running': self.running.value == 1
        }
        return info

    def update(self, gameinfo):
        self.carta = gameinfo['carta_mesa']
        self.contador = gameinfo['contador']
        self.running = gameinfo['is_running']
        

    


#clase jugador 
class Player():
    def __init__(self, nombre):
        self.nombre = nombre 
        self.mano = []
    
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
#print(mazo.muestraCarta())

j1 = Player("Maria")
#print(j1.__str__())

j1.robar(7,mazo.cartas)
print(j1.__str__())
     

tablero = Tablero()
print("La carta del tablero es:")
print(tablero.carta.__str__()) #muestra la carta del tablero 

j1.echar_carta (tablero)
print(j1.__str__())

print(tablero.carta.__str__())

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
            idd,gameinfo = conn.recv()
            print(f"I am playing {idd}")
            tablero.update(gameinfo)
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
                #display.refresh()
                #display.tick()
    except:
        traceback.print_exc()
    finally:
        pygame.quit() #duda como cerrarlo


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)

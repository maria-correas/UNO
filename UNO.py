#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 20:02:04 2022

@author: mat
"""

"""
EL UNO VERSIÓN RÁPIDA

"""
#from random import random
#import numpy as np

jugadores = 2
 
        

#clase carta
class Carta():
    
    colores = ["Azul", "Amarillo" , "Rojo", "Verde"]
    valores = ["1","2","3","4","5","6","7","8","9", "Bloqueo", "+2"]
    
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
    
    def muestraCarta(self): #muestra la ultima carta 
        return f" {self.cartas[-1].valor} {self.cartas[-1].color}"

         
    def __str__2 (self):
        for carta in self.cartas:
            carta.__str__()


#clase tablero 
class Tablero(Carta):
    def __init__(self):
        import random
        self.carta = Carta(random.choice(self.valores),random.choice(self.colores))
    


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
        if (carta.valor == tablero.carta.valor) or (carta.color == tablero.carta.color):
            return True
        return False

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

    
    
    
    
    
    
    
    
    
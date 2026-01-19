import random
import os 


class Laberinto:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas 
        self.tablero = self.crear_tablero()
        self.inicio = (0,0)
        self.fin = (filas - 1, columnas - 1)
        self.tablero[0][0]= 'S'
        self.tablero[filas - 1][columnas - 1]
    

    def crear_tablero(self):
        return [[" " for _ in range(self.columnas) ]for _ in range(self.filas)]
    
    def mostrar_tablero(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        encabezado = " "
        for i in range(self.columnas):
            encabezado += f"{i:<3}"
        print(encabezado)

        for i, fila in enumerate(self.tablero):
            fila_texto = f"{i:<3}"
            for celda in fila:
                fila_texto += celda + " "
            print(fila_texto) 
    
    def agregar_obstaculos(self, fila, columna, tipo):
        if not ( 0 <= fila < self.filas and 0 <= columna < self.columnas): return False
        
        if self.tablero[fila][columna] in [ "S" , "E" ]: return False
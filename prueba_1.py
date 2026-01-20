import random
import os

class Laberinto:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tablero = self.crear_tablero()
        self.inicio = (0, 0)
        self.fin = (filas - 1, columnas - 1)
        self.tablero[0][0] = "S"
        self.tablero[filas - 1][columnas - 1] = "E"
        
    def crear_tablero(self):
        """Crea un tablero básico lleno de caminos vacíos"""
        return [[" " for _ in range(self.columnas)] for _ in range(self.filas)]
    
    def mostrar_tablero(self):
        """Muestra el tablero en la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Imprimir números de columnas arriba
        encabezado = "   "
        for i in range(self.columnas):
            encabezado += f"{i:<2}"
        print(encabezado)
        
        # Imprimir cada fila con su número
        for i, fila in enumerate(self.tablero):
            fila_texto = f"{i:<3}"
            for celda in fila:
                fila_texto += celda + " "
            print(fila_texto)
    
    def agregar_obstaculo(self, fila, columna, tipo):
        """Agrega un obstáculo al tablero
        
        Args:
            fila: Posición de la fila
            columna: Posición de la columna
            tipo: Tipo de obstáculo ('#' para muro, '~' para agua)
        
        Returns:
            bool: True si se agregó correctamente, False si no
        """
        if not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            return False
        
        if self.tablero[fila][columna] in ["S", "E"]:
            return False
        
        self.tablero[fila][columna] = tipo
        return True
    
    def reiniciar_tablero(self):
        """Reinicia el tablero manteniendo solo inicio y fin"""
        self.tablero = self.crear_tablero()
        self.tablero[self.inicio[0]][self.inicio[1]] = "S"
        self.tablero[self.fin[0]][self.fin[1]] = "E"
    
    def resolver_bfs(self):
        """Resuelve el laberinto usando BFS (Breadth-First Search)
        
        Returns:
            bool: True si encontró un camino, False si no existe camino
        """
        cola = [self.inicio]
        visitados = {self.inicio: None}
        
        while cola:
            actual = cola.pop(0)
            if actual == self.fin:
                break
            
            f, c = actual
            # Direcciones: arriba, abajo, izquierda, derecha
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nf, nc = f + df, c + dc
                if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                    # Se puede pasar por espacio vacío o agua (~)
                    if self.tablero[nf][nc] in [" ", "~", "E"] and (nf, nc) not in visitados:
                        visitados[(nf, nc)] = actual
                        cola.append((nf, nc))
        
        # Reconstruir el camino
        if self.fin not in visitados:
            return False
        
        paso = self.fin
        while paso:
            f, c = paso
            if self.tablero[f][c] not in ["S", "E"]:
                self.tablero[f][c] = "."
            paso = visitados[paso]
        
        return True
    
    def jugar(self):
        """Inicia el bucle principal del juego"""
        while True:
            self.mostrar_tablero()
            print("\n[1] Añadir Muro (#) | [2] Añadir Agua (~) | [3] Resolver laberinto | [4] Salir")
            opcion = input("Elige una opción: ")
            
            if opcion == "4":
                print("¡Hasta luego!")
                break
            
            if opcion == "3":
                # Resolver el laberinto
                self.reiniciar_tablero()
                exito = self.resolver_bfs()
                self.mostrar_tablero()
                
                if exito:
                    print("\n¡Camino encontrado! Marcado con puntos (.).")
                else:
                    print("\nNo existe un camino posible con esos obstáculos.")
                
                input("\nPresiona Enter para continuar...")
                continue
            
            if opcion in ["1", "2"]:
                tipo = "#" if opcion == "1" else "~"
                try:
                    f_obj = int(input(f"Fila del objeto (0-{self.filas - 1}): "))
                    c_obj = int(input(f"Columna del objeto (0-{self.columnas - 1}): "))
                    
                    if self.agregar_obstaculo(f_obj, c_obj, tipo):
                        print(f"{'Muro' if tipo == '#' else 'Agua'} agregado correctamente.")
                    else:
                        print("¡No puedes colocar un obstáculo en esa posición!")
                    
                except ValueError:
                    print("Coordenadas no válidas.")
                except IndexError:
                    print("Coordenadas fuera de rango.")


# --- FLUJO PRINCIPAL ---
if __name__ == "__main__":
    print("=== JUEGO DEL LABERINTO ===")
    f = int(input('¿Cuántas filas tendrá el mapa?: '))
    c = int(input('¿Cuántas columnas tendrá el mapa?: '))
    
    laberinto = Laberinto(f, c)
    laberinto.jugar()
import os
from abc import ABC, abstractmethod


# ============================================
# CLASE MAPA
# ============================================
class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tablero = [[" " for _ in range(columnas)] for _ in range(filas)]
        self.inicio = (0, 0)
        self.fin = (filas - 1, columnas - 1)
        self.tablero[0][0] = "S"
        self.tablero[filas - 1][columnas - 1] = "E"
    
    def agregar_obstaculo(self, f, c, tipo):
        if 0 <= f < self.filas and 0 <= c < self.columnas:
            if self.tablero[f][c] not in ["S", "E"]:
                self.tablero[f][c] = tipo
                return True
        return False
    
    def es_accesible(self, f, c):
        if not (0 <= f < self.filas and 0 <= c < self.columnas):
            return False
        return self.tablero[f][c] in [" ", "~", "E"]
    
    def reiniciar(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] == ".":
                    self.tablero[i][j] = " "
        self.tablero[0][0] = "S"
        self.tablero[self.fin[0]][self.fin[1]] = "E"


# ============================================
# HERENCIA - Algoritmos de búsqueda
# ============================================
class AlgoritmoBusqueda(ABC):
    def __init__(self, mapa):
        self.mapa = mapa
    
    @abstractmethod
    def encontrar_ruta(self, inicio, fin):
        pass
    
    def _reconstruir_camino(self, visitados, inicio, fin):
        if fin not in visitados:
            return None
        camino = []
        paso = fin
        while paso:
            camino.append(paso)
            paso = visitados[paso]
        return camino[::-1]


class BusquedaBFS(AlgoritmoBusqueda):
    def encontrar_ruta(self, inicio, fin):
        cola = [inicio]
        visitados = {inicio: None}
        
        while cola:
            actual = cola.pop(0)
            if actual == fin:
                return self._reconstruir_camino(visitados, inicio, fin)
            
            f, c = actual
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nf, nc = f + df, c + dc
                if self.mapa.es_accesible(nf, nc) and (nf, nc) not in visitados:
                    visitados[(nf, nc)] = actual
                    cola.append((nf, nc))
        return None





# ============================================
# CALCULADORA DE RUTAS
# ============================================
class CalculadoraDeRutas:
    def __init__(self, mapa, algoritmo):
        self.mapa = mapa
        self.algoritmo = algoritmo
    
    def calcular_ruta(self):
        return self.algoritmo.encontrar_ruta(self.mapa.inicio, self.mapa.fin)
    
    def marcar_camino(self, camino):
        if camino:
            for f, c in camino:
                if self.mapa.tablero[f][c] not in ["S", "E"]:
                    self.mapa.tablero[f][c] = "."
            return True
        return False


# ============================================
# VISTA
# ============================================
class Vista:
    def mostrar_mapa(self, mapa):
        os.system('cls' if os.name == 'nt' else 'clear')
        encabezado = "   "
        for i in range(mapa.columnas):
            encabezado += f"{i:<3}"
        print(encabezado)
        
        for i, fila in enumerate(mapa.tablero):
            texto = f"{i:<3}"
            for celda in fila:
                texto += celda + "  "
            print(texto)
    
    def mostrar_menu(self):
        print("\n[1] Muro (#) | [2] Agua (~) | [3] BFS | [5] Salir")
        return input("Opción: ")
    
    def pedir_coordenadas(self, max_f, max_c):
        f = int(input(f"Fila (0-{max_f}): "))
        c = int(input(f"Columna (0-{max_c}): "))
        return f, c


# ============================================
# JUEGO
# ============================================
class Juego:
    def __init__(self, mapa, vista):
        self.mapa = mapa
        self.vista = vista
        self.bfs = BusquedaBFS(mapa)
    
    def jugar(self):
        while True:
            self.vista.mostrar_mapa(self.mapa)
            opcion = self.vista.mostrar_menu()
            
            if opcion == "5":
                print("¡Adiós!")
                break
            
            if opcion in ["1", "2"]:
                tipo = "#" if opcion == "1" else "~"
                try:
                    f, c = self.vista.pedir_coordenadas(self.mapa.filas - 1, self.mapa.columnas - 1)
                    if self.mapa.agregar_obstaculo(f, c, tipo):
                        print(f"✓ {'Muro' if tipo == '#' else 'Agua'} agregado")
                    else:
                        print("✗ No se puede colocar ahí")
                except:
                    print("✗ Error en coordenadas")
            
            elif opcion in ["3"]:
                self.mapa.reiniciar()
                algoritmo = self.bfs
                nombre = "BFS"
                
                calc = CalculadoraDeRutas(self.mapa, algoritmo)
                camino = calc.calcular_ruta()
                self.vista.mostrar_mapa(self.mapa)
                
                if calc.marcar_camino(camino):
                    self.vista.mostrar_mapa(self.mapa)
                    print(f"✓ Camino encontrado ({len(camino)} pasos) - {nombre}")
                else:
                    print("✗ No hay camino posible")
                input("\nEnter para continuar...")


# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print("\n=== LABERINTO ===\n")
    try:
        f = int(input('Filas: '))
        c = int(input('Columnas: '))
        
        if f >= 2 and c >= 2:
            mapa = Mapa(f, c)
            vista = Vista()
            juego = Juego(mapa, vista)
            juego.jugar()
        else:
            print("Mínimo 2x2")
    except:
        print("Error en datos")
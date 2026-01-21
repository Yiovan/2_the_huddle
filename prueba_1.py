import os
from abc import ABC, abstractmethod


# ============================================
# 1. CLASE MAPA - Responsabilidad: Gestionar el tablero
# ============================================
class Mapa:
    """Representa el tablero del laberinto con sus obstáculos"""
    
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tablero = self._crear_tablero()
        self.inicio = (0, 0)
        self.fin = (filas - 1, columnas - 1)
        self._inicializar_puntos()
    
    def _crear_tablero(self):
        """Crea un tablero vacío"""
        return [[" " for _ in range(self.columnas)] for _ in range(self.filas)]
    
    def _inicializar_puntos(self):
        """Marca los puntos de inicio y fin"""
        self.tablero[self.inicio[0]][self.inicio[1]] = "S"
        self.tablero[self.fin[0]][self.fin[1]] = "E"
    
    def agregar_obstaculo(self, fila, columna, tipo):
        """Agrega un obstáculo en la posición especificada"""
        if not self._es_posicion_valida(fila, columna):
            return False
        
        if self.tablero[fila][columna] in ["S", "E"]:
            return False
        
        self.tablero[fila][columna] = tipo
        return True
    
    def quitar_obstaculo(self, fila, columna):
        """Quita un obstáculo de la posición especificada"""
        if not self._es_posicion_valida(fila, columna):
            return False
        
        if self.tablero[fila][columna] not in ["S", "E"]:
            self.tablero[fila][columna] = " "
            return True
        return False
    
    def es_accesible(self, fila, columna):
        """Verifica si una celda es accesible"""
        if not self._es_posicion_valida(fila, columna):
            return False
        return self.tablero[fila][columna] in [" ", "~", "E"]
    
    def _es_posicion_valida(self, fila, columna):
        """Verifica si las coordenadas están dentro del tablero"""
        return 0 <= fila < self.filas and 0 <= columna < self.columnas
    
    def reiniciar(self):
        """Reinicia el tablero manteniendo los obstáculos"""
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] == ".":
                    self.tablero[i][j] = " "
        self._inicializar_puntos()
    
    def marcar_camino(self, camino):
        """Marca el camino en el tablero"""
        for fila, columna in camino:
            if self.tablero[fila][columna] not in ["S", "E"]:
                self.tablero[fila][columna] = "."


# ============================================
# 2. CLASE RUTA - Representa un camino encontrado
# ============================================
class Ruta:
    """Representa una ruta desde inicio hasta fin"""
    
    def __init__(self, camino):
        self.camino = camino
    
    def obtener_coordenadas(self):
        """Devuelve la lista de coordenadas del camino"""
        return self.camino
    
    def obtener_longitud(self):
        """Devuelve la longitud del camino"""
        return len(self.camino) if self.camino else 0
    
    def es_valida(self):
        """Verifica si la ruta es válida"""
        return self.camino is not None and len(self.camino) > 0


# ============================================
# 3. HERENCIA - Algoritmos de búsqueda
# ============================================
class AlgoritmoBusqueda(ABC):
    """Clase base abstracta para algoritmos de búsqueda"""
    
    def __init__(self, mapa):
        self.mapa = mapa
    
    @abstractmethod
    def encontrar_ruta(self, inicio, fin):
        """Encuentra una ruta desde inicio hasta fin"""
        pass
    
    def _reconstruir_camino(self, visitados, inicio, fin):
        """Reconstruye el camino desde fin hasta inicio"""
        if fin not in visitados:
            return None
        
        camino = []
        paso = fin
        while paso is not None:
            camino.append(paso)
            paso = visitados[paso]
        return camino[::-1]


class BusquedaBFS(AlgoritmoBusqueda):
    """Implementación de búsqueda en anchura (BFS)"""
    
    def encontrar_ruta(self, inicio, fin):
        """Encuentra la ruta más corta usando BFS"""
        cola = [inicio]
        visitados = {inicio: None}
        
        while cola:
            actual = cola.pop(0)
            
            if actual == fin:
                camino = self._reconstruir_camino(visitados, inicio, fin)
                return Ruta(camino)
            
            fila, columna = actual
            
            # Explorar vecinos (arriba, abajo, izquierda, derecha)
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nueva_fila = fila + df
                nueva_columna = columna + dc
                vecino = (nueva_fila, nueva_columna)
                
                if self.mapa.es_accesible(nueva_fila, nueva_columna) and vecino not in visitados:
                    visitados[vecino] = actual
                    cola.append(vecino)
        
        return Ruta(None)


class BusquedaDFS(AlgoritmoBusqueda):
    """Implementación de búsqueda en profundidad (DFS)"""
    
    def encontrar_ruta(self, inicio, fin):
        """Encuentra una ruta usando DFS"""
        pila = [inicio]
        visitados = {inicio: None}
        
        while pila:
            actual = pila.pop()
            
            if actual == fin:
                camino = self._reconstruir_camino(visitados, inicio, fin)
                return Ruta(camino)
            
            fila, columna = actual
            
            # Explorar vecinos (arriba, abajo, izquierda, derecha)
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nueva_fila = fila + df
                nueva_columna = columna + dc
                vecino = (nueva_fila, nueva_columna)
                
                if self.mapa.es_accesible(nueva_fila, nueva_columna) and vecino not in visitados:
                    visitados[vecino] = actual
                    pila.append(vecino)
        
        return Ruta(None)


# ============================================
# 4. CLASE CALCULADORA DE RUTAS
# ============================================
class CalculadoraDeRutas:
    """Gestiona el cálculo de rutas usando diferentes algoritmos"""
    
    def __init__(self, mapa, algoritmo):
        self.mapa = mapa
        self.algoritmo = algoritmo
    
    def calcular_ruta_mas_corta(self):
        """Calcula la ruta más corta desde inicio hasta fin"""
        return self.algoritmo.encontrar_ruta(self.mapa.inicio, self.mapa.fin)
    
    def cambiar_algoritmo(self, nuevo_algoritmo):
        """Permite cambiar el algoritmo de búsqueda"""
        self.algoritmo = nuevo_algoritmo


# ============================================
# 5. CLASE VISTA - Responsabilidad: Mostrar información
# ============================================
class VistaLaberinto:
    """Maneja toda la visualización del laberinto"""
    
    def limpiar_pantalla(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_mapa(self, mapa):
        """Muestra el mapa del laberinto"""
        self.limpiar_pantalla()
        
        # Encabezado con números de columnas
        encabezado = "   "
        for i in range(mapa.columnas):
            encabezado += f"{i:<3}"
        print(encabezado)
        
        # Filas del tablero
        for i, fila in enumerate(mapa.tablero):
            fila_texto = f"{i:<3}"
            for celda in fila:
                fila_texto += celda + "  "
            print(fila_texto)
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("[1] Añadir Muro (#)")
        print("[2] Añadir Agua (~)")
        print("[3] Quitar Obstáculo")
        print("[4] Resolver con BFS (ruta más corta)")
        print("[5] Resolver con DFS")
        print("[6] Salir")
        print("="*50)
        return input("Elige una opción: ")
    
    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje al usuario"""
        print(f"\n{mensaje}")
    
    def mostrar_ruta_encontrada(self, ruta):
        """Muestra información sobre la ruta encontrada"""
        if ruta.es_valida():
            self.mostrar_mensaje(f"¡Camino encontrado! Longitud: {ruta.obtener_longitud()} pasos")
            self.mostrar_mensaje("Marcado con puntos (.)")
        else:
            self.mostrar_mensaje("No existe un camino posible con esos obstáculos.")
    
    def pedir_coordenadas(self, max_fila, max_columna):
        """Pide coordenadas al usuario"""
        fila = int(input(f"Fila (0-{max_fila}): "))
        columna = int(input(f"Columna (0-{max_columna}): "))
        return fila, columna
    
    def pausar(self):
        """Pausa hasta que el usuario presione Enter"""
        input("\nPresiona Enter para continuar...")


# ============================================
# 6. CLASE JUEGO - Responsabilidad: Coordinar todo
# ============================================
class Juego:
    """Coordina la lógica del juego del laberinto"""
    
    def __init__(self, mapa, vista):
        self.mapa = mapa
        self.vista = vista
        self.algoritmo_bfs = BusquedaBFS(mapa)
        self.algoritmo_dfs = BusquedaDFS(mapa)
        self.calculadora = CalculadoraDeRutas(mapa, self.algoritmo_bfs)
    
    def _manejar_agregar_obstaculo(self, tipo):
        """Maneja la lógica de agregar un obstáculo"""
        try:
            fila, columna = self.vista.pedir_coordenadas(
                self.mapa.filas - 1, 
                self.mapa.columnas - 1
            )
            
            if self.mapa.agregar_obstaculo(fila, columna, tipo):
                nombre = 'Muro' if tipo == '#' else 'Agua'
                self.vista.mostrar_mensaje(f"✓ {nombre} agregado correctamente.")
            else:
                self.vista.mostrar_mensaje("✗ No puedes colocar un obstáculo en esa posición.")
        
        except ValueError:
            self.vista.mostrar_mensaje("✗ Coordenadas no válidas.")
        except Exception as e:
            self.vista.mostrar_mensaje(f"✗ Error: {e}")
    
    def _manejar_quitar_obstaculo(self):
        """Maneja la lógica de quitar un obstáculo"""
        try:
            fila, columna = self.vista.pedir_coordenadas(
                self.mapa.filas - 1, 
                self.mapa.columnas - 1
            )
            
            if self.mapa.quitar_obstaculo(fila, columna):
                self.vista.mostrar_mensaje("✓ Obstáculo eliminado correctamente.")
            else:
                self.vista.mostrar_mensaje("✗ No hay obstáculo en esa posición o es un punto especial.")
        
        except ValueError:
            self.vista.mostrar_mensaje("✗ Coordenadas no válidas.")
        except Exception as e:
            self.vista.mostrar_mensaje(f"✗ Error: {e}")
    
    def _manejar_resolver(self, tipo_algoritmo):
        """Maneja la lógica de resolver el laberinto"""
        self.mapa.reiniciar()
        
        # Cambiar algoritmo según la opción
        if tipo_algoritmo == "BFS":
            self.calculadora.cambiar_algoritmo(self.algoritmo_bfs)
        else:
            self.calculadora.cambiar_algoritmo(self.algoritmo_dfs)
        
        # Calcular ruta
        ruta = self.calculadora.calcular_ruta_mas_corta()
        
        # Mostrar resultado
        self.vista.mostrar_mapa(self.mapa)
        
        if ruta.es_valida():
            self.mapa.marcar_camino(ruta.obtener_coordenadas())
            self.vista.mostrar_mapa(self.mapa)
            self.vista.mostrar_ruta_encontrada(ruta)
            self.vista.mostrar_mensaje(f"Algoritmo usado: {tipo_algoritmo}")
        else:
            self.vista.mostrar_ruta_encontrada(ruta)
        
        self.vista.pausar()
    
    def jugar(self):
        """Método principal del juego"""
        while True:
            self.vista.mostrar_mapa(self.mapa)
            opcion = self.vista.mostrar_menu()
            
            if opcion == "6":
                self.vista.mostrar_mensaje("¡Hasta luego!")
                break
            
            elif opcion == "1":
                self._manejar_agregar_obstaculo("#")
            
            elif opcion == "2":
                self._manejar_agregar_obstaculo("~")
            
            elif opcion == "3":
                self._manejar_quitar_obstaculo()
            
            elif opcion == "4":
                self._manejar_resolver("BFS")
            
            elif opcion == "5":
                self._manejar_resolver("DFS")
            
            else:
                self.vista.mostrar_mensaje("✗ Opción no válida.")
                self.vista.pausar()


# ============================================
# PROGRAMA PRINCIPAL
# ============================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  LABERINTO - SISTEMA DE BÚSQUEDA DE RUTAS")
    print("="*50)
    
    try:
        filas = int(input('\nCuántas filas tendrá el mapa: '))
        columnas = int(input('Cuántas columnas tendrá el mapa: '))
        
        if filas < 2 or columnas < 2:
            print("El mapa debe tener al menos 2x2.")
        else:
            # Crear instancias de todas las clases
            mapa = Mapa(filas, columnas)
            vista = VistaLaberinto()
            juego = Juego(mapa, vista)
            
            # Iniciar el juego
            juego.jugar()
    
    except ValueError:
        print("Por favor ingresa números válidos.")
    except KeyboardInterrupt:
        print("\n\n¡Juego interrumpido!")
    except Exception as e:
        print(f"Error inesperado: {e}")
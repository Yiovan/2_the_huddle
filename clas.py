class CuentaBancaria:
    # El "molde" pide el nombre del titular y un saldo inicial
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular  # Atributo: Quién es el dueño
        self.saldo = saldo_inicial  # Atributo: Cuánto dinero tiene 


    def depositar(self, cantidad):
        if cantidad > 0:
            self.saldo += cantidad
            print(f"✅ Depósito exitoso. Nuevo saldo de {self.titular}: ${self.saldo}")
        else:
            print("❌ La cantidad debe ser mayor a cero.")

    def consultar_saldo(self):
        print(f'el saldo de {self.titular} es de :$ {self.saldo}')



cuenta_name = CuentaBancaria("Yio", 5000)

cuenta_name.depositar()
cuenta_name.consultar_saldo()



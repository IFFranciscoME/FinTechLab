

class Nodo(object):

    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None

    def insertar(self, dato):
        if self.dato:
            if self.izq is None:
                self.izq = Nodo(dato)
            elif self.der is None:
                self.der = Nodo(dato)
            else:
                self.izq.insertar(dato)
        else:
            self.dato = dato

    def buscar(self, dato):
        """
        :param dato: dato a buscar

        :return: resultado de buscar_contar o False
        """
        # Validar si existe el dato en el nodo
        if self.dato is not None:
            return self.buscar_contar(dato, ruta='', conteo=0)
        else:
            return False

    def buscar_contar(self, dato, ruta, conteo):
        # print('entra a buscar_contar')
        # print('El valor de self.dato es: ' + str(self.dato))
        # print('El valor de dato es: ' + str(dato))

        if self.dato:
            ruta += ('-' + str(self.dato))
            # print(ruta)
            if self.dato == dato:
                # print('entra al if')
                # conteo += 1
                return ruta, True
            else:
                if self.izq is not None:
                    return self.izq.buscar_contar(dato, ruta, conteo)
                elif self.der is not None:
                    return self.der.buscar_contar(dato, ruta, conteo)
                else:
                    # print('else previo final')
                    return ruta, False
                    # return False
        else:
            print('else final')
            return ruta, conteo
            # return False

    def minimo(self):
        if self.dato is not None:
            # print('self.dato existe, con: ' + str(self.dato))
            if self.izq is not None and self.izq.dato is not None and self.izq.dato <= self.dato:
                return self.izq.minimo()
            if self.der is not None and self.der.dato is not None and self.der.dato <= self.dato:
                return self.der.minimo()
            return self.dato

    def incidencias(self, dato, conteo):

        # Validar si existe el dato en el nodo
        if self.dato is not None:
            if self.incidencias_contar(dato, conteo):
                conteo += 1
                if self.izq:
                    return self.izq.incidencias(dato, conteo)
                elif self.der:
                    return self.der.incidencias(dato, conteo)
                else:
                    return conteo
            else:
                return conteo
        else:
            return conteo

    def incidencias_contar(self, dato, conteo):

        if self.dato == dato:
            print(str(self.dato) + ' == ' + str(dato))
            return True
        else:
            if self.izq:
                return self.izq.incidencias_contar(dato, conteo)
            elif self.der:
                return self.der.incidencias_contar(dato, conteo)
            else:
                return False


arbol = Nodo(10)
arbol.insertar(1)
arbol.insertar(1)
arbol.insertar(1)
arbol.insertar(7)
arbol.insertar(6)
arbol.insertar(0)
arbol.insertar(9)
arbol.insertar(8)
arbol.insertar(2)
arbol.insertar(2)

# -- Ejercicio 1
print(arbol.minimo())

# -- Ejercicio 2
dato_b = 11
ruta_en, conteo_en = arbol.buscar(dato_b)
print('el numero a buscar fue : ' + str(dato_b))
print('el conteo de ocurrencias fue : ' + str(conteo_en))
print('la ruta tomada fue: ' + str(ruta_en))

# -- Ejercicio 3
cantidad = arbol.incidencias(1, conteo=0)
print('las incidencias encontradas con el algoritmo simple fueron: ' + str(cantidad))

import random as rn
import numpy as np


class Funtions:

    # CONSTRUCTOR
    def __init__(self):
        print()

    # METODO PARA GENERAR PESOS
    def Generar_pesos(self, row, col):
        Matriz = []
        for N in range(row):
            Fila = []
            for M in range(col):
                Fila.append(round(rn.uniform(-1, 1), 2))
            Matriz.append(Fila)
        return Matriz

    # METODO PARA GENERAR UMBRALES
    def Generar_umbrales(self, col):
        Fila = []
        for M in range(col):
            Fila.append(round(rn.uniform(-1, 1), 2))
        return Fila

    # NORMALIZAR ENTRADAS
    def NormalizarMatrices(self, entrada):
        entradas = []
        for i in range(len(entrada[0])):
            aux = []
            for j in range(len(entrada)):
                aux.append(entrada[j][i])
            entradas.append(aux)
        return entradas

    def FuncionSoma(self, entradas, pesos, umbrales):
        salidaSoma = []
        for i in range(len(pesos[0])):
            sumatoria = 0
            for j in range(len(pesos)):
                sumatoria += entradas[j] * pesos[j][i]
            salidaSoma.append(sumatoria - umbrales[i])
        return salidaSoma

    # METODO PARA OBTENER LA FUNCION ESCALON
    def FuncionEscalon(self, salidaSoma):
        yr = []
        for i in range(len(salidaSoma)):
            yr.append(1 if salidaSoma[i] >= 0 else 0)
        return yr

    # METODO PARA OBTENER LA FUNCION SIGMOIDE
    def FuncionSigmoide(self, salidaSoma):
        yr = []
        for i in range(len(salidaSoma)):
            yr.append(1 / (1 + np.exp(-salidaSoma[i])))
        return yr

    # METODO PARA OBTENER LA FUNCION LINEAL
    def FuncionLineal(self, salidaSoma):
        yr = salidaSoma
        return yr

    # NOMBRE DE LA FUNCION SALIDA
    def FuncionSalida(self, funcionSalida, salidaSoma):
        switcher = {
            'ESCALON': self.FuncionEscalon(salidaSoma),
            'LINEAL': self.FuncionLineal(salidaSoma),
            'SIGMOIDE': self.FuncionSigmoide(salidaSoma)
        }
        return switcher.get(funcionSalida, "ERROR")

    # METODO PARA OBTENER EL ERROR LINAL
    def ErrorLineal(self, salidas, salidaSoma):
        error = []
        for salida, soma in zip(salidas, salidaSoma):
            error.append(salida - soma)
        return error

    # METODO PARA OBTENER EL ERROR PATRON
    def ErrorPatron(self, salidas):
        error = 0
        for salida in salidas:
            error += abs(salida)
        return error / len(salidas)

    def ActualizarPesos(self, pesos, entradas, error, rata):
        _pesos = []
        for i in range(len(pesos)):
            fila = []
            for j in range(len(pesos[0])):
                fila.append(pesos[i][j] + (entradas[i] * error[j] * rata))
            _pesos.append(fila)
        return _pesos

    def ActualizarUmbrales(self, umbrales, error, rata):
        _umbrales = []
        for i in range(len(umbrales)):
            _umbrales.append(umbrales[i] + (1 * error[i] * rata))
        return _umbrales

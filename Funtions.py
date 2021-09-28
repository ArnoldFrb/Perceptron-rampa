import random as rn
import numpy as np


class Funtions:

    # CONSTRUCTOR
    def __init__(self):
        print()

    # METODO PARA GENERAR PESOS
    def Generar_pesos(self, row, col):
        return np.random.uniform(-1, 1, [row, col])

    # NORMALIZAR ENTRADAS
    def NormalizarMatrices(self, entrada):
        entradas = []
        for i in range(len(entrada[0])):
            aux = []
            for j in range(len(entrada)):
                aux.append(entrada[j][i])
            entradas.append(aux)
        return entradas

    def FuncionSoma(self, entradas, pesos):
        salidaSoma = []
        for i in range(len(pesos[0])):
            sumatoria = 0
            for j in range(len(pesos)):
                sumatoria += entradas[j] * pesos[j][i]
            salidaSoma.append(sumatoria)
        return salidaSoma

    # METODO PARA OBTENER LA FUNCION ESCALON
    def FuncionEscalon(self, salidaSoma):
        yr = []
        for i in range(len(salidaSoma)):
            yr.append(1 if salidaSoma[i] >= 0 else 0)
        return yr

    # METODO PARA OBTENER LA FUNCION ESCALON
    def FuncionRampa(self, salidaSoma, entrada, rampa):
        yr = []
        for i in range(len(salidaSoma)):
            if salidaSoma[i] < 0:
                yr.append(0)
            if salidaSoma[i] >= 0 and salidaSoma[i] <= 1:
                yr.append(entrada if rampa else salidaSoma[i])
            if salidaSoma[i] > 1:
                yr.append(1)
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
    def FuncionSalida(self, funcionSalida, salidaSoma, entrada, rampa):
        switcher = {
            'ESCALON': self.FuncionEscalon(salidaSoma),
            'LINEAL': self.FuncionLineal(salidaSoma),
            'SIGMOIDE': self.FuncionSigmoide(salidaSoma),
            'RAMPA': self.FuncionRampa(salidaSoma, entrada, rampa)
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
            error += np.abs(salida)
        return error / len(salidas)

    def ActualizarPesos(self, pesos, entradas, error, rata):
        for i in range(len(pesos)):
            for j in range(len(pesos[0])):
                pesos[i][j] += (entradas[i] * error[j] * rata)
        return pesos


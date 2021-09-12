import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from heapq import nsmallest
from Funtions import *
import pandas as pd
from tkinter import ttk
import tkinter as tk

class Neorona:

    #CONSTRUCTOR
    def __init__(self):
        self.Entradas = []
        self.func = Funtions()
    

    # LLENAR MATRICES ENTRADAS
    def NormalizarDatos(self, ruta):
        self.Entradas = []
        self.Salidas = []
        Matriz = pd.read_csv(ruta, delimiter=' ')
        col = Matriz.columns
        column = Matriz.to_numpy()
        self.Entranamiento = os.path.basename(os.path.splitext(ruta)[0])

        for i in range(len(col)):
            Fila = []
            if('X' in col[i]):
                for j in range(len(column)):
                    Fila.append(column[j,i])
                self.Entradas.append(Fila)
            else:
                for j in range(len(column)):
                    Fila.append(column[j,i])
                self.Salidas.append(Fila)
            

    # INICIAR ENTRENAMIENTO
    def Entrenar(self, rataAprendizaje, coeficieteVecindad, neuronas, numeroIteraciones, funcionSalida, frame):

        ###################################
        frameBarra = tk.Frame(frame, width=550, height=50, background="#fafafa")
        frameBarra.place(relx=.15, rely=0)
        barra = ttk.Progressbar(frameBarra, maximum=numeroIteraciones)
        barra.place(relx=.01, rely=.05, width=514)
        #####################################

        self.Entradas = (self.func.NormalizarMatrices(self.Entradas))
        print('ENTRADAS:')
        print(np.array(self.Entradas))
        print()

        self.Salidas = self.func.NormalizarMatrices(self.Salidas)
        print('SALIDAS:')
        print(np.array(self.Salidas))
        print()
        
        # INICIALIZAR PESOS
        pesos = self.func.Generar_pesos(len(self.Entradas[0]), len(self.Salidas[0]))
        print('PESOS:')
        print(pesos)
        print()

        # INICIALIZAR UMBRALES
        umbrales = self.func.Generar_umbrales(len(self.Salidas[0]))
        print('UMBRALES:')
        print(umbrales)
        print()

        print('FUNCION SALIDA:', funcionSalida)
        print()

        GraficaError = []
        plt.style.use('ggplot')
        plt.grid(True)

        Iteracion = 1

        while True:

            barra.step()
            self.DistanciasGanadoras = []
            Error = 0

            print('ITERACION:', Iteracion)
            print()

            for entrada, salida in zip(self.Entradas, self.Salidas):
                print('PATRON:', entrada, '=>', salida)
                print()

                salidaSoma = self.func.FuncionSoma(entrada, pesos, umbrales)
                print('SALIDA SOMA:', salidaSoma)
                print()

                _salidaSoma = self.func.FuncionSalida(funcionSalida, salidaSoma)
                print('SALIDA:', _salidaSoma)
                print()

                errorLineal = self.func.ErrorLineal(salida, _salidaSoma)
                print('ERROR LINEAL:', errorLineal)
                print()

                errorPatron = self.func.ErrorPatron(_salidaSoma)
                print('ERROR DEL PATRON:', errorPatron)
                print()

                pesos = self.func.ActualizarPesos(pesos, entrada, errorLineal, rataAprendizaje)
                print('NUEVOS PESOS:', pesos)
                print()

                umbrales = self.func.ActualizarUmbrales(umbrales, errorLineal, rataAprendizaje)
                print('NUEVOS UMBRALES:', umbrales)
                print()

                Iteracion += 1
                print('------------------------------------')
                print()
            
            
            Error = sum(self.DistanciasGanadoras) / len(self.Entradas)
            tk.Label(frameBarra, text='Error: ' + str(round(Error, 7)), bg="#fafafa").place(relx=.15, rely=.6)
            tk.Label(frameBarra, text='Iteracion: ' + str(Iteracion), bg="#fafafa").place(relx=.65, rely=.6)
            Iteracion += 1

            GraficaError.append(Error)
            line, = plt.plot(GraficaError)
            plt.pause(0.005)
            plt.cla()

            print()
            print('///////////////////////////////////////////////')
            print('RATA ACTUALIZADA:', rataAprendizaje)
            print('DISTANCIAS GANADORAS:', self.DistanciasGanadoras, '/', len(self.Entradas))
            print('ERROR:', Error)
            print()

            if((Iteracion > numeroIteraciones) or (Error <= 0.0001)):
                self.GuardarResultados(pesos, self.Entradas, coeficieteVecindad)

            #CONDICIONES DE PARADA
            if((Iteracion > numeroIteraciones) or (Error <= 0.0001)):
                break

        print('ITERACIONES:', Iteracion-1)
        print('ERROR FINAL:', Error)
    # LLENAR MATRICES ENTRADAS
    def NormalizarDatosSimulacion(self, ruta):
        self.EntradasSimulacion = []
        self.PesosSimulacion = []

        MatrizEntradas = pd.read_excel(ruta, sheet_name='Entradas')
        MatrizPesos = pd.read_excel(ruta, sheet_name='Pesos')
        MatrizCoeficiente = pd.read_excel(ruta, sheet_name='Configuracion')

        colEntradas = MatrizEntradas.columns
        colPesos = MatrizPesos.columns
        colCoe = MatrizCoeficiente.columns

        columnEntradas = MatrizEntradas.to_numpy()
        columnPesos = MatrizPesos.to_numpy()
        columnCoe = MatrizCoeficiente.to_numpy()

        for i in range(len(colEntradas)):
            Fila = []
            for j in range(len(columnEntradas)):
                Fila.append(columnEntradas[j,i])
            self.EntradasSimulacion.append(Fila)

        for i in range(len(colPesos)):
            Fila = []
            for j in range(len(columnPesos)):
                Fila.append(columnPesos[j,i])
            self.PesosSimulacion.append(Fila)

        for i in range(len(colCoe)):
            Fila = []
            for j in range(len(columnCoe)):
                self.Coe = columnCoe[j,i]

    def Simular(self, ruta, coeficieteVecindad):

        plt.style.use('ggplot')
        plt.grid(True)

        self.NormalizarDatosSimulacion(ruta)

        self.EntradasSimulacion = self.func.NormalizarMatrices(self.EntradasSimulacion)
        self.PesosSimulacion = self.func.NormalizarMatrices(self.PesosSimulacion)

        print('//////////////////////////////////////////////////////')
        print('----------------------SIMULACION----------------------')
        print()

        self.DistanciasGanadorasSimulacion = []

        for entrada in self.EntradasSimulacion:
            print('PATRON:', entrada)
            print()

            DistanciaEuclidiana = self.func.DistanciaEuclidiana(entrada, self.PesosSimulacion)

            NeuronaVencedora = np.array(DistanciaEuclidiana).flat[np.abs(np.array(DistanciaEuclidiana) - self.Coe).argmin()]
            self.DistanciasGanadorasSimulacion.append(NeuronaVencedora)

            print('DISTANCIA VENCEDOR:')
            print(self.DistanciasGanadorasSimulacion)


    def GuardarResultados(self, pesos, entradas, coeficiete):
        ColumnasPeso = []
        ColumnaEntradas = []

        for i in range(len(pesos[0])):
            ColumnasPeso.append('W' + str(i+1))

        for i in range(len(entradas[0])):
            ColumnaEntradas.append('X' + str(i+1))
        
        df = pd.DataFrame(entradas, columns=ColumnaEntradas)
        _df = pd.DataFrame(pesos, columns=ColumnasPeso)
        df_ = pd.DataFrame([coeficiete], columns=['Config'])

        with pd.ExcelWriter('DATA/OUT/' + self.Entranamiento + '.xlsx') as writer: # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name='Entradas', index=False)
            _df.to_excel(writer, sheet_name='Pesos', index=False)
            df_.to_excel(writer, sheet_name='Configuracion', index=False)

    # LIMPIAR CAPAS
    def Limpiar(self):
        self.capas = []  

if __name__ == '__main__':
    print("Hola")
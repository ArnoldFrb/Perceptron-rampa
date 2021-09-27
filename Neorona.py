import os
import errno
import copy as cp
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

from tkinter import ttk
from Funtions import *

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
        
        self.Entradas = (self.func.NormalizarMatrices(cp.deepcopy(self.Entradas)))
        self.Salidas = self.func.NormalizarMatrices(cp.deepcopy(self.Salidas))
            
    # INICIAR ENTRENAMIENTO
    def Entrenar(self, rataAprendizaje, errorMaximo, numeroIteraciones, funcionSalida, frame):

        ###################################
        frameBarra = tk.Frame(frame, width=550, height=50, background="#fafafa")
        frameBarra.place(relx=.15, rely=0)
        barra = ttk.Progressbar(frameBarra, maximum=numeroIteraciones)
        barra.place(relx=.01, rely=.05, width=514)
        #####################################
        
        # INICIALIZAR PESOS
        pesos = self.func.Generar_pesos(len(self.Entradas[0]), len(self.Salidas[0]))
       
        # INICIALIZAR UMBRALES
        umbrales = self.func.Generar_umbrales(len(self.Salidas[0]))

        GraficaError = []
        plt.style.use('ggplot')
        plt.grid(True)

        Iteracion = 1

        while True:

            barra.step()
            self.errorRMS = []
            self.vsSalidas = []

            for entrada, salida in zip(self.Entradas, self.Salidas):

                salidaSoma = self.func.FuncionSoma(entrada, pesos, umbrales)
                _salidaSoma = self.func.FuncionSalida(funcionSalida, salidaSoma)
                self.vsSalidas.append([sum(salida), sum(_salidaSoma)])

                errorLineal = self.func.ErrorLineal(salida, _salidaSoma)
                errorPatron = self.func.ErrorPatron(errorLineal)
                self.errorRMS.append(errorPatron)

                pesos = self.func.ActualizarPesos(cp.deepcopy(pesos), entrada, errorLineal, rataAprendizaje)
                umbrales = self.func.ActualizarUmbrales(cp.deepcopy(umbrales), errorLineal, rataAprendizaje)

            Error = sum(self.errorRMS) / len(self.Entradas)
            tk.Label(frameBarra, text='Error: ' + str(round(Error, 7)), bg="#fafafa").place(relx=.15, rely=.6)
            tk.Label(frameBarra, text='Iteracion: ' + str(Iteracion), bg="#fafafa").place(relx=.65, rely=.6)
            
            Iteracion += 1

            GraficaError.append(Error)
            line, = plt.plot(GraficaError)
            plt.pause(0.0005)
            plt.cla()

            #CONDICIONES DE PARADA
            if Iteracion > numeroIteraciones or errorMaximo > Error:
                if errorMaximo > Error:
                    self.GuardarResultados(np.array(self.Entradas), pesos, umbrales, funcionSalida)
                break

    # LLENAR MATRICES ENTRADAS
    def NormalizarDatosSimulacion(self, ruta):
        self.EntradasSimulacion = []
        self.SalidasSimulacion = []
        self.PesosSimulacion = []
        self.UmbralesSimulacion = []

        Matriz = pd.read_excel(ruta, sheet_name='Matriz')
        MatrizPesos = pd.read_excel(ruta, sheet_name='Pesos')
        MatrizUmbrales = pd.read_excel(ruta, sheet_name='Umbrales')
        MatrizFuncionActivacion = pd.read_excel(ruta, sheet_name='Configuracion')

        colMatriz = Matriz.columns
        colPesos = MatrizPesos.columns
        colFuncionActivacion = MatrizFuncionActivacion.columns


        columnMatriz = Matriz.to_numpy()
        columnPesos = MatrizPesos.to_numpy()
        columnUmbrales = MatrizUmbrales.to_numpy()
        columnFuncionActivacion = MatrizFuncionActivacion.to_numpy()

        for i in range(len(colMatriz)):
            Fila = []
            for j in range(len(columnMatriz)):
                Fila.append(columnMatriz[j,i])
            self.EntradasSimulacion.append(Fila)

        for i in range(len(colPesos)):
            Fila = []
            for j in range(len(columnPesos)):
                Fila.append(columnPesos[j,i])
            self.PesosSimulacion.append(Fila)
        
        for i in range(len(columnUmbrales)):
            self.UmbralesSimulacion.append(columnUmbrales[i][0])

        for i in range(len(colFuncionActivacion)):
            Fila = []
            for j in range(len(columnFuncionActivacion)):
                self.FuncionActivacionSimulacion = columnFuncionActivacion[j,i]

    def Simular(self, ruta, errorMaximo):

        plt.style.use('ggplot')
        plt.grid(True)

        self.NormalizarDatosSimulacion(ruta)

        self.EntradasSimulacion = self.func.NormalizarMatrices(self.EntradasSimulacion)
        self.PesosSimulacion = self.func.NormalizarMatrices(self.PesosSimulacion)

        print('//////////////////////////////////////////////////////')
        print('----------------------SIMULACION----------------------')
        print()

        self.SalidasGeneradas = []

        for entrada in self.EntradasSimulacion:
                salidaSoma = self.func.FuncionSoma(entrada, self.PesosSimulacion, self.UmbralesSimulacion)
                _salidaSoma = self.func.FuncionSalida(self.FuncionActivacionSimulacion, salidaSoma)
                self.SalidasGeneradas.append(sum(_salidaSoma))

        print('SALIDAS:')
        print(self.SalidasGeneradas)


    def GuardarResultados(self, entradas, pesos, umbrales, funcionSalida):
        ColumnaMatriz = []
        ColumnasPeso = []

        for i in range(len(entradas[0])):
            ColumnaMatriz.append('X' + str(i+1))

        for i in range(len(pesos[0])):
            ColumnasPeso.append('W' + str(i+1))
        
        dfMatrix = pd.DataFrame(entradas, columns=ColumnaMatriz)
        dfPesos = pd.DataFrame(pesos, columns=ColumnasPeso)
        dfUmbrales = pd.DataFrame(umbrales, columns=['U'])
        dfConfig = pd.DataFrame([funcionSalida], columns=['Config'])

        try:
            os.mkdir('DATA/OUT')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        with pd.ExcelWriter('DATA/OUT/' + self.Entranamiento + '.xlsx') as writer: # pylint: disable=abstract-class-instantiated
            dfMatrix.to_excel(writer, sheet_name='Matriz', index=False)
            dfPesos.to_excel(writer, sheet_name='Pesos', index=False)
            dfUmbrales.to_excel(writer, sheet_name='Umbrales', index=False)
            dfConfig.to_excel(writer, sheet_name='Configuracion', index=False)

if __name__ == '__main__':
    print(np.random.uniform(-1,1,[2]))
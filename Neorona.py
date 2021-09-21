from datetime import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import errno
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
    def Entrenar(self, rataAprendizaje, errorMaximo, numeroIteraciones, funcionSalida, frame):

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
            self.errorRMS = []
            self.vsSalidas = []
            Error = 0

            print('ITERACION:', Iteracion)
            print('------------------------------------------------------------------------')
            print('------------------------------------------------------------------------')
            print()

            for entrada, salida in zip(self.Entradas, self.Salidas):
                print('PATRON:', entrada, '=>', salida)
                print()

                salidaSoma = self.func.FuncionSoma(entrada, pesos, umbrales)
                self.vsSalidas.append([sum(salida), sum(salidaSoma)])
                print('SALIDA SOMA:', salidaSoma)
                print()

                _salidaSoma = self.func.FuncionSalida(funcionSalida, salidaSoma)
                print('SALIDA:', _salidaSoma)
                print()

                errorLineal = self.func.ErrorLineal(salida, _salidaSoma)
                print('ERROR LINEAL:', errorLineal)
                print()

                errorPatron = self.func.ErrorPatron(_salidaSoma)
                self.errorRMS.append(errorPatron)
                print('ERROR DEL PATRON:', errorPatron)
                print()

                pesos = self.func.ActualizarPesos(pesos, entrada, errorLineal, rataAprendizaje)
                print('NUEVOS PESOS:', pesos)
                print()

                umbrales = self.func.ActualizarUmbrales(umbrales, errorLineal, rataAprendizaje)
                print('NUEVOS UMBRALES:', umbrales)
                print()

                print('------------------------------------')
                print()
            
            
            Error = sum(self.errorRMS) / len(self.Entradas)
            tk.Label(frameBarra, text='Error: ' + str(round(Error, 7)), bg="#fafafa").place(relx=.15, rely=.6)
            tk.Label(frameBarra, text='Iteracion: ' + str(Iteracion), bg="#fafafa").place(relx=.65, rely=.6)
            Iteracion += 1

            GraficaError.append(Error)
            line, = plt.plot(GraficaError)
            plt.pause(0.0005)
            plt.cla()

            print()
            print('///////////////////////////////////////////////')
            print('ERROR: ', self.errorRMS, '/', len(self.Entradas), 'ERROR RMS:', Error)
            print()

            #CONDICIONES DE PARADA
            if((Iteracion > numeroIteraciones) or (Error <= errorMaximo)):
                self.GuardarResultados(self.Entradas, self.Salidas, pesos, umbrales, funcionSalida)
                break

        print('ITERACIONES:', Iteracion-1)
        print('ERROR FINAL:', Error)
        print()

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
        colUmbrales = MatrizUmbrales.columns
        colFuncionActivacion = MatrizFuncionActivacion.columns


        columnMatriz = Matriz.to_numpy()
        columnPesos = MatrizPesos.to_numpy()
        columnUmbrales = MatrizUmbrales.to_numpy()
        columnFuncionActivacion = MatrizFuncionActivacion.to_numpy()

        for i in range(len(colMatriz)):
            Fila = []
            if('X' in colMatriz[i]):
                for j in range(len(columnMatriz)):
                    Fila.append(columnMatriz[j,i])
                self.EntradasSimulacion.append(Fila)
            else:
                for j in range(len(columnMatriz)):
                    Fila.append(columnMatriz[j,i])
                self.SalidasSimulacion.append(Fila)

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
        self.SalidasSimulacion = self.func.NormalizarMatrices(self.SalidasSimulacion)
        self.PesosSimulacion = self.func.NormalizarMatrices(self.PesosSimulacion)

        print('//////////////////////////////////////////////////////')
        print('----------------------SIMULACION----------------------')
        print()

        self.SalidasGeneradas = []

        for entrada in self.EntradasSimulacion:
                salidaSoma = self.func.FuncionSoma(entrada, self.PesosSimulacion, self.UmbralesSimulacion)
                self.SalidasGeneradas.append(salidaSoma)

        print('SALIDAS:')
        print(self.SalidasGeneradas)


    def GuardarResultados(self, entradas, salidas, pesos, umbrales, funcionSalida):
        ColumnaMatriz = []
        ColumnasPeso = []

        for i in range(len(entradas[0]) + len(salidas[0])):
            ColumnaMatriz.append('X' + str(i+1) if i < len(entradas[0]) else 'YD' + str(i+1-len(entradas[0])))

        for i in range(len(pesos[0])):
            ColumnasPeso.append('W' + str(i+1))
        
        dfMatrix = pd.DataFrame(np.concatenate((np.array(entradas), np.array(salidas)), axis=1), columns=ColumnaMatriz)
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

    # LIMPIAR CAPAS
    def Limpiar(self):
        self.capas = []  

if __name__ == '__main__':
    print("Hola")
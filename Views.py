import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

from matplotlib.pyplot import legend
from Neorona import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Views:

    def __init__(self, window):
        self.wind = window
        self.wind.title("PERCEPTRON UNICAPA")
        self.wind.resizable(0,0)
        self.wind.geometry("1100x600")
        self.wind.winfo_screenheight()
        self.wind.winfo_screenwidth()
        self.neuro = Neorona()

        # FRAME PRINCIPAL
        frameMain = tk.Frame(master=self.wind, width=1100, height=600, background="#e3e3e3")
        frameMain.place(relx=.0, rely=.0)

        # FRAME PARQ CONFIGURAR LA RATA DE APREN., NUMERO DE ITERA. Y ERROR MAXIMO
        self.frameConfig = tk.Frame(frameMain, width=450, height=50, background="#fafafa")
        self.frameConfig.place(relx=.01, rely=.02)

        tk.Label(self.frameConfig, text="PARAMETROS DE ENTRENAMIENTO", bg="#fafafa").place(relx=.01, rely=.001)

        btnData = tk.Button(self.frameConfig, text="Cargar Data", command= self.Event_btnData,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        btnData.place(relx=.01, rely=.4)

        tk.Label(self.frameConfig, text="RATA:", bg="#fafafa").place(relx=.2, rely=.5)
        self.entRataAprendizaje = tk.Entry(self.frameConfig, width=5)
        self.entRataAprendizaje.place(relx=.3, rely=.5)
        self.entRataAprendizaje.insert(0, 1)

        tk.Label(self.frameConfig, text="ERROR:", bg="#fafafa").place(relx=.47, rely=.5)
        self.errorMaximo = tk.Entry(self.frameConfig, width=6)
        self.errorMaximo.place(relx=.57, rely=.5)
        self.errorMaximo.insert(0, 0.001)

        tk.Label(self.frameConfig, text="ITERA:", bg="#fafafa").place(relx=.75, rely=.5)
        self.entIteraciones = tk.Entry(self.frameConfig, width=10)
        self.entIteraciones.place(relx=.85, rely=.5)
        self.entIteraciones.insert(0, 1000)

        # FRAME PARA VISUALIZAR ENTRADAS, SALIDAS Y PATRONES
        self.frameConfigInicial = tk.Frame(frameMain, width=450, height=60, background="#fafafa")
        self.frameConfigInicial.place(relx=.01, rely=.115)

        tk.Label(self.frameConfigInicial, text="CONFIG ENTRENAMIENTO", bg="#fafafa").place(relx=.34, rely=.01)
        tk.Label(self.frameConfigInicial, text="ENTRADAS", bg="#fafafa").place(relx=.01, rely=.35)
        tk.Label(self.frameConfigInicial, text="SALIDAS", bg="#fafafa").place(relx=.21, rely=.35)
        tk.Label(self.frameConfigInicial, text="PATRONES", bg="#fafafa").place(relx=.4, rely=.35)
        self.cobBoxCompetencia = ttk.Combobox(self.frameConfigInicial)
        self.cobBoxCompetencia["values"] = ['ESCALON', 'LINEAL', 'SIGMOIDE', 'RAMPA']
        self.cobBoxCompetencia.place(relx=.63, rely=.35)
        self.cobBoxCompetencia.insert(0, "RAMPA")

        # FRAME PARA VISUALIZAR LOS DATOS DE ENTRENAMIENTO
        self.frameData = tk.Frame(frameMain, background="#fafafa", width=450, height=264)
        self.frameData.place(relx=.01, rely=.227)

        # FRAME PARA CONFIGURAR Y VISUALIZAR LAS CAPAS Y FUNCIONES DE ACTIVACION
        self.frameConfigSimulacion = tk.Frame(frameMain, width=450, height=180, background="#fafafa")
        self.frameConfigSimulacion.place(relx=.01, rely=.678)

        tk.Label(self.frameConfigSimulacion, text="SIMULACION", bg="#fafafa").place(relx=.02, rely=.01)

        self.btnAgregar = tk.Button(self.frameConfigSimulacion, text="Simular", command= self.Event_btnSimular,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnAgregar.place(relx=.870, rely=.01)

        self.btnLimpiar = tk.Button(self.frameConfigSimulacion, text="Cargar Datos", command= self.Event_btnCargarDatos,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
        self.btnLimpiar.place(relx=.685, rely=.01)

        # FRAME PARQA VISUALIZAR LA CONFIGURACION DE LAS CAPAS
        self.frameTableSimulacion = tk.Frame(self.frameConfigSimulacion, width=450, height=144, background="#fafafa")
        self.frameTableSimulacion.place(relx=0, rely=.2)

        self.frameEntrenar = tk.Frame(frameMain, width=620, height=50, background="#fafafa")
        self.frameEntrenar.place(relx=.426, rely=.02)

        self.btnEntrenar = tk.Button(self.frameEntrenar, text="Entrenar", state=tk.DISABLED, command= self.Event_btnEntrenar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=0)
        self.btnEntrenar.place(relx=.01, rely=.03)

        self.btnPausar = tk.Button(self.frameEntrenar, text="Detener", state=tk.DISABLED, command= self.Event_btnPausar,
         relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=0)
        self.btnPausar.place(relx=.01, rely=.52)

        self.frameEntranamiento = tk.Frame(frameMain, width=620, height=228, background="#fafafa")
        self.frameEntranamiento.place(relx=.426, rely=.115)

        self.frameSimulacion = tk.Frame(frameMain, width=620, height=283, background="#fafafa")
        self.frameSimulacion.place(relx=.426, rely=.506)

    def Event_btnData(self):
        
        self.ruta = filedialog.askopenfilename()
        self.neuro.NormalizarDatos(self.ruta)

        tk.Label(self.frameConfig, text=os.path.basename(os.path.splitext(self.ruta)[0]), bg="#fafafa").place(relx=.85, rely=.01)

        Matriz = pd.read_csv(self.ruta, delimiter=' ')
        
        if 'YD1' not in Matriz.columns:
            messagebox.showinfo(message="No se encuentra salidas definidas en la matriz presentada.", title="ERROR")
            return

        treeView = ttk.Treeview(self.frameData)
        self.CrearGrid(treeView, self.frameData)
        self.LlenarTabla(treeView, Matriz)

        tk.Label(self.frameConfigInicial, text=str(len(self.neuro.Entradas[0])), bg="#fafafa").place(relx=.148, rely=.35)
        tk.Label(self.frameConfigInicial, text=str(len(self.neuro.Salidas[0])), bg="#fafafa").place(relx=.32, rely=.35)
        tk.Label(self.frameConfigInicial, text=str(len(self.neuro.Salidas)), bg="#fafafa").place(relx=.54, rely=.35)

        self.btnEntrenar['state'] = tk.NORMAL

    def Event_btnEntrenar(self):
        self.btnPausar['state'] = tk.NORMAL

        rta = int(self.entRataAprendizaje.get())
        erm = float(self.errorMaximo.get())
        ite = int(self.entIteraciones.get())

        if(rta > 1):
            messagebox.showinfo(message="La Rata de Aprendizaje debe ser igual a 1 o menor", title="ERROR")
            return

        self.neuro.Entrenar(rta, erm, ite, self.cobBoxCompetencia.get(), self.frameEntrenar)
        self.Graficar(self.frameEntranamiento, self.neuro.vsSalidas)
    
    def Event_btnPausar(self):
        return

    def Event_btnCargarDatos(self):
        self._ruta = filedialog.askopenfilename()
        Matriz = pd.read_excel(self._ruta, sheet_name='Matriz')

        treeView = ttk.Treeview(self.frameTableSimulacion)
        self.CrearGrid(treeView, self.frameTableSimulacion)
        self.LlenarTabla(treeView, Matriz)

    def Event_btnSimular(self):
        self.neuro.Simular(self._ruta, float(self.errorMaximo.get()))
        self.Graficar(self.frameSimulacion, self.neuro.SalidasGeneradas)
    
    def LlenarTabla(self, treeView, Matriz):
        treeView.delete(*treeView.get_children())
        treeView["column"] = list(Matriz.columns)
        treeView["show"] = "headings"

        for column in treeView["columns"]:
            treeView.column(column=column, width=10, anchor='center')
            treeView.heading(column=column, text=column)

        Matriz_rows1 = Matriz.to_numpy().tolist()
        for row in Matriz_rows1:
            treeView.insert("", "end", values=row)

    def CrearGrid(self, treeView, frame):
        style = ttk.Style(frame)
        style.configure(treeView, rowheight=100, highlightthickness=0, bd=0)  
        treeView.place(relheight=1, relwidth=1)

    def Graficar(self, frame, data):
        fig = Figure(figsize=(5, 4), dpi=100)
        if np.array(data).ndim == 2:
            fig.add_subplot(111).plot([fila[0] for fila in data], 'o', [fila[1] for fila in data], '^')
        else:
            fig.add_subplot(111).plot(data, 'o')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(relwidth=1, relheight=1)

    def Event_btnLimpiar(self):
        self.neuro.Limpiar()

if __name__ == '__main__':
    winw = tk.Tk()
    Views(winw)
    winw.mainloop()
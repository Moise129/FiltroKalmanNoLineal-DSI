from tkinter import *  
from tkinter import ttk, font
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from module_python.proceso_real import Pelota
from module_python.filtrado import Filtro

import threading
import copy

class Ventana:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Filtro Kalman Lineal")
        self.fuente = font.Font(weight='bold')
        self.ventana.configure(bg = 'beige')
        self.dt = DoubleVar()
        self.sx = DoubleVar()
        self.svx = DoubleVar()
        self.sy = DoubleVar()
        self.svy = DoubleVar()

        self.x_real = []
        self.y_real = []

        self.x_predicha = []
        self.y_predicha = []

        self.x_predicha_uscented = []
        self.y_predicha_uscented = []

        self.pelota = None
        self.inicializar_variables()
        self.seccion_configuracion()
    
    def inicializar_variables(self):
        self.dt.set(1.0)
        self.sx.set(10)
        self.svx.set(20)
        self.sy.set(10)
        self.svy.set(20)

    def obtener_valor_variables(self):
        dt = float(self.dt.get())
        sx = float(self.sx.get()) / 100
        svx = float(self.svx.get()) / 100
        sy = float(self.sy.get()) / 100
        svy = float(self.svy.get()) / 100
        return dt,sx,svx,sy,svy

    def seccion_configuracion(self):
        Label(self.ventana, text="Filtro Kalman Lineal",font=self.fuente).grid(pady=5, row=0, column=0,columnspan=2)
        f_configuration = ttk.Frame(self.ventana, borderwidth=2, padding=(5,5))
        f_configuration.grid( pady=5, row=2, column=0,columnspan=2)
        #Label(f_configuration, text="Configuracion",font=fuente).grid(pady=5, row=0, column=0,columnspan=3)
        self.seccion_variables_constantes(f_configuration)
        self.seccion_de_condiciones_iniciales(f_configuration)
        Button(self.ventana, text="Iniciar Filtro", width=50, bg="green",command=self.accion_boton).grid(padx=10, pady=10, row=3, column=0, columnspan=2)
    

    def seccion_variables_constantes(self,f_configuration):
        f_configuration_init = ttk.Frame(f_configuration, borderwidth=2, padding=(5,5))
        f_configuration_init.grid( pady=5, row=1, column=1)
        Label(f_configuration_init, text="----------",font=self.fuente).grid(pady=5,padx=15, row=0, column=0,columnspan=2)

        Label(f_configuration_init, text="dt:").grid( pady=5, row=1, column=0)
        entry_dt = Entry(f_configuration_init,textvariable=self.dt, width=10)
        entry_dt.grid(padx=5, row=1, column=1)
        Label(f_configuration_init, text="..").grid(pady=5, row=2, column=0,columnspan=2)


    def seccion_de_condiciones_iniciales(self,f_configuration):
        f_configuration_cond_init = ttk.Frame(f_configuration, borderwidth=2, padding=(5,5))
        f_configuration_cond_init.grid( pady=5, row=1, column=2)
        Label(f_configuration_cond_init, text="Condiciones Iniciales",font=self.fuente).grid(pady=5,padx=15, row=0, column=0,columnspan=6)


        Label(f_configuration_cond_init, text="sx:").grid(pady=5, row=1, column=4)
        Label(f_configuration_cond_init, text="svx:").grid( pady=5, row=2, column=4)
        entry_sx = Entry(f_configuration_cond_init,textvariable=self.sx, width=10)
        entry_sx.grid(padx=5, row=1, column=5)
        entry_svx = Entry(f_configuration_cond_init,textvariable=self.svx, width=10)
        entry_svx.grid(padx=5, row=2, column=5)

        Label(f_configuration_cond_init, text="sy:").grid(pady=5, row=1, column=6)
        Label(f_configuration_cond_init, text="svy:").grid( pady=5, row=2, column=6)
        entry_sy = Entry(f_configuration_cond_init,textvariable=self.sy, width=10)
        entry_sy.grid(padx=5, row=1, column=7)
        entry_svy = Entry(f_configuration_cond_init,textvariable=self.svy, width=10)
        entry_svy.grid(padx=5, row=2, column=7)

    def reiniciar_arreglos(self):
        self.x_real = []
        self.y_real = []
        self.x_predicha = []
        self.y_predicha = []
        self.x_predicha_uscented = []
        self.y_predicha_uscented = []

    def accion_boton(self):
        self.reiniciar_arreglos()
        dt,sx,svx,sy,svy = self.obtener_valor_variables()

        self.pelota = Pelota()
        filtro = Filtro( self.pelota.Xk, self.pelota.σQ, self.pelota.F)
        
        #self.filtro = Filtro(self.pelota.Xk, self.pelota.σQ, self.pelota.F)

        for i in range(10):
            #self.graficar_por_iteracion()

            filtro.iniciar_proceso(self.pelota.Zk)
            
            #filtro.imprimir_resultados()

            self.x_real.append(self.pelota.Xk[0][0].copy()) #Real
            self.y_real.append(self.pelota.Xk[1][0].copy()) #Real
            print("X real: ", self.x_real[i])
            print("y real: ", self.y_real[i])
            self.x_predicha.append(filtro.predicha[0][0].copy()) #Predicha
            self.y_predicha.append(filtro.predicha[1][0].copy()) #Predicha
            self.x_predicha_uscented.append(filtro.Xˆk[0][0].copy()) #Estimada
            self.y_predicha_uscented.append(filtro.Xˆk[1][0].copy()) #Estimada
            print("X estimada: ", self.x_predicha_uscented[i])
            print("Y estimada: ", self.y_predicha_uscented[i])

            
            print("X predicha: ", self.x_predicha[i])
            print("X predicha: ", self.y_predicha[i])


            print("-----------------------------------------")

            #print(id(filtro.X),id(filtro.Xˆk))
            self.pelota.obtener_estado(self.pelota.Xk)
            

        """ print("X real: ", self.x_real)
        print("Y Real: ", self.y_real)
        print("X Predicha: ", self.x_predicha)
        print("Y Predicha: ", self.y_predicha)
        print("X Estimada: ", self.x_predicha_uscented)
        print("Y Estimada: ", self.y_predicha_uscented) """

        self.graficar()
        #self.tabla_de_datos()
        
    def graficar_por_iteracion(self):
        #plt.figure()   #  Añade un nuevo gráfico y lo activa
        plt.cla()
        plt.ion()
        plt.grid()
        plt.plot(copy.copy(self.x_real), copy.copy(self.y_real), marker='.',color='r') #marker='.'
        plt.plot(copy.copy(self.x_predicha), copy.copy(self.y_predicha), marker='.',color='g')
        plt.plot(copy.copy(self.x_predicha_uscented), copy.copy(self.y_predicha_uscented), marker='.',color='b')
        plt.legend(('Real', 'Predicha','Estimada'), prop = {'size': 10}, loc='upper left')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Grafico Comparativo")
        plt.show()
        plt.pause(0.05)
        
        

    def graficar(self):
        """ print("X real: ", self.x_real)
        print("Y Real: ", self.y_real)
        print("X Predicha: ", self.x_predicha)
        print("Y Predicha: ", self.y_predicha)
        print("X Estimada: ", self.x_predicha_uscented)
        print("Y Estimada: ", self.y_predicha_uscented) """
        plt.figure()   #  Añade un nuevo gráfico y lo activa
        plt.grid()
        plt.plot(self.x_real, self.y_real, marker='.', linestyle=":",color='r') #marker='.'
        plt.plot(self.x_predicha_uscented, self.y_predicha_uscented , marker='.', linestyle=":",color='b') # estimada
        plt.plot(self.x_predicha, self.y_predicha, marker='.', linestyle=":",color='g') # predicha
        plt.legend(('Real', 'Predicha','Estimada'), prop = {'size': 10}, loc='upper left')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Grafico Comparativo")
        #plt.close()
        plt.show()



    def tabla_de_datos(self):
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.axis('tight')

        parametros= np.arange(len(self.x_real))
        df = pd.DataFrame({'Caso x' : np.array(self.x_real).tolist(),
                        'Caso y' : np.array(self.y_real).tolist(),
                        'Caso x1' : np.array(self.x_predicha).tolist(),
                        'Caso y1' : np.array(self.y_predicha).tolist(),
                        'Caso x2' : np.array(self.x_predicha_uscented).tolist(),
                        'Caso y2' : np.array(self.y_predicha_uscented).tolist()})

        ax.table(cellText=df.values, rowLabels=parametros, colLabels=df.columns, cellLoc='center', loc='center')
        fig.tight_layout()
        plt.show()

if __name__ == '__main__':
    root = Tk()
    app = Ventana(root)
    root.update()
    root.deiconify()
    root.mainloop()
from tkinter import *  
from tkinter import ttk, font
import matplotlib.pyplot as plt

from module_python.pelota import Pelota
from module_python.jugador import Jugador
from module_python.filtro import Filtro
import threading

class Ventana:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Filtro Kalman Lineal")
        self.fuente = font.Font(weight='bold')
        self.ventana.configure(bg = 'beige')
        self.t = DoubleVar()
        self.dt = DoubleVar()
        self.g = DoubleVar()
        self.x = DoubleVar()
        self.y = DoubleVar()
        self.vx = DoubleVar()
        self.vy = DoubleVar()
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
        self.t.set(1.3)
        self.dt.set(1.0)
        self.g.set(9.81)
        self.x.set(1)
        self.y.set(1)
        self.vx.set(1)
        self.vy.set(1)
        self.sx.set(10)
        self.svx.set(10)
        self.sy.set(20)
        self.svy.set(20)

    def obtener_valor_variables(self):
        dt = float(self.dt.get())
        x = float(self.x.get())
        y = float(self.y.get())
        vx = float(self.vx.get())
        vy = float(self.vy.get())
        sx = float(self.sx.get()) / 100
        svx = float(self.svx.get()) / 100
        sy = float(self.sy.get()) / 100
        svy = float(self.svy.get()) / 100
        return dt,x,y,vx,vy,sx,svx,sy,svy

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
        Label(f_configuration_init, text="Constantes",font=self.fuente).grid(pady=5,padx=15, row=0, column=0,columnspan=2)

        Label(f_configuration_init, text="dt:").grid( pady=5, row=1, column=0)
        entry_dt = Entry(f_configuration_init,textvariable=self.dt, width=10)
        entry_dt.grid(padx=5, row=1, column=1)
        Label(f_configuration_init, text="..").grid(pady=5, row=2, column=0,columnspan=2)


    def seccion_de_condiciones_iniciales(self,f_configuration):
        f_configuration_cond_init = ttk.Frame(f_configuration, borderwidth=2, padding=(5,5))
        f_configuration_cond_init.grid( pady=5, row=1, column=2)
        Label(f_configuration_cond_init, text="Condiciones Iniciales",font=self.fuente).grid(pady=5,padx=15, row=0, column=0,columnspan=6)

        Label(f_configuration_cond_init, text="x:").grid(pady=5, row=1, column=0)
        Label(f_configuration_cond_init, text="vx:").grid( pady=5, row=2, column=0)
        entry_x = Entry(f_configuration_cond_init,textvariable=self.x, width=10)
        entry_x.grid(padx=5, row=1, column=1)
        entry_vx = Entry(f_configuration_cond_init,textvariable=self.vx, width=10)
        entry_vx.grid(padx=5, row=2, column=1)

        Label(f_configuration_cond_init, text="y:").grid(pady=5, row=1, column=2)
        Label(f_configuration_cond_init, text="vy:").grid( pady=5, row=2, column=2)
        entry_y = Entry(f_configuration_cond_init,textvariable=self.y, width=10)
        entry_y.grid(padx=5, row=1, column=3)
        entry_vy = Entry(f_configuration_cond_init,textvariable=self.vy, width=10)
        entry_vy.grid(padx=5, row=2, column=3)

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

    def accion_boton(self):
        self.reiniciar_arreglos()
        dt,x,y,vx,vy,sx,svx,sy,svy = self.obtener_valor_variables()
        self.pelota = Pelota(dt,x,y,vx,vy,sx,svx,sy,svy)
        print(self.pelota.vector_x)
        """ pelota = Pelota(dt,x,y,vx,vy,sx,svx,sy,svy)
        t = threading.Thread(target=pelotita.obtener_estado(pelota.vector_x))
        t.start() """
        for i in range(10):
            self.pelota.obtener_estado(self.pelota.vector_x)
            self.x_real.append(self.pelota.vector_x[0][0])
            self.y_real.append(self.pelota.vector_x[1][0])

            jugador = Jugador(self.pelota.matriz_f, self.pelota.vector_x,0,1,1,1,self.pelota.vector_sigma)
            filtro_unscented = Filtro(1,self.pelota.vector_x[0][0],self.pelota.vector_x[1][0],self.pelota.vector_sigma[0][0],self.pelota.vector_sigma[1][0])
            
            self.x_predicha.append(jugador.vector_prediccion_x[0][0])
            self.y_predicha.append(jugador.vector_prediccion_x[1][0])

            self.x_predicha_uscented.append(filtro_unscented.Xˆk[0][0])
            self.y_predicha_uscented.append(filtro_unscented.Xˆk[1][0])

        print("X real: ", self.x_real)
        print("Y Real: ", self.y_real)
        print("X Predicha: ", self.x_predicha)
        print("Y Predicha: ", self.y_predicha)
        print("X Predicha unscented: ", self.x_predicha_uscented)
        print("Y Predicha unscented: ", self.y_predicha_uscented)

        self.graficar()

    def graficar(self):
        plt.figure()   #  Añade un nuevo gráfico y lo activa
        plt.grid()
        plt.plot(self.x_real,self.y_real, linestyle='-',color='r',marker='*') #marker='.'
        plt.plot(self.x_predicha,self.y_predicha, linestyle='--',color='g')
        plt.plot(self.x_predicha_uscented,self.y_predicha_uscented,linestyle='-',color='b')
        plt.legend(('Real', 'Predicha','ud'), prop = {'size': 10}, loc='upper left')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Grafico Comparativo")
        plt.show()

if __name__ == '__main__':
    root = Tk()
    app = Ventana(root)
    root.update()
    root.deiconify()
    root.mainloop()
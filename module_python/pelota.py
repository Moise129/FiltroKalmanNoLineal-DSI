from scipy.stats import norm
from prettytable import PrettyTable
import numpy as np
import time

class Pelota():
    def __init__(self,dt,x,y,vx,vy,sx,svx,sy,svy): #,sx,svx,sy,svy
        self.matriz_f =np.array([[x,0,vx,0],[0,y,0,vy],[0,0,vx,0],[0,0,0,vy]])
        self.vector_sigma = np.array([[sx],[sy],[svx],[svy]])
        self.vector_w = np.array(
            [
                [np.random.normal(0,self.vector_sigma[0][0])],
                [np.random.normal(0,self.vector_sigma[1][0])],
                [np.random.normal(0,self.vector_sigma[2][0])],
                [np.random.normal(0,self.vector_sigma[3][0])],
            ]
        )

        #[np.random.normal(0,self.vector_sigma,4)]
        print("Iniciando:       ",self.vector_w)
          #norm(self.vector_sigma) # verificar que si se requiere s*s o s (en forma de matriz)
        self.vector_x = np.array([[x],[y],[vx],[vy]])
        self.area=0

    def obtener_estado(self,vector_x):
        self.vector_w = np.array(
            [
                [np.random.normal(0,self.vector_sigma[0][0])],
                [np.random.normal(0,self.vector_sigma[1][0])],
                [np.random.normal(0,self.vector_sigma[2][0])],
                [np.random.normal(0,self.vector_sigma[3][0])],
            ]
        )
        self.vector_x =(np.matmul(self.matriz_f,vector_x)) + self.vector_w
        #self.imprimir_resultados()
        time.sleep(0.004)

    def imprimir_resultados(self):
        table = PrettyTable()
        table.field_names = ["x","y","vx","vy"]
        for i in range(0,4):
            table.add_row(
                [
                    str(self.matriz_f[i][0]),
                    str(self.matriz_f[i][1]),
                    str(self.matriz_f[i][2]),
                    str(self.matriz_f[i][3])
                ]
            )
        print(table)
        print(self.vector_x)
        print("Vector W:  ",self.vector_w)
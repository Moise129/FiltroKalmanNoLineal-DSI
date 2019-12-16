import numpy as np
from prettytable import PrettyTable
import math


class Pelota():
    #Δ=delta  && σ=sigma
    def __init__(self,Δt=1,σx=0.10,σvx=0.10,σy=0.20,σvy=0.20): 
        self.F = np.array([[1,0,Δt,0],[0,1,0,Δt],[0,0,1,0],[0,0,0,1]]) 

        self.σQ = np.array([[σx],[σy],[σvx],[σvy]])  #Vector sigmas
        self.W = np.random.normal(0,self.σQ)
        self.σR = np.array([[σx],[σy],[0],[0]]) **2 #,[σvx],[σvy]
        self.V = np.random.normal(0,self.σR)
        self.Xk = None
        self.Zk = None

        self.obtener_estado( np.array([[1],[1],[1],[1]]) )
        self.imprimir_resultados()

    def obtener_estado(self, Xk_1):
        self.W = np.random.normal(0,self.σQ)
        self.V = np.random.normal(0,self.σR)

        self.Xk = (np.matmul(self.F, Xk_1)) + self.W ## vector de estado (4*1)
        _Xk = self.Xk.copy() #Generando una copia

        self.Zk = self.H(self.Xk) + self.V  # vector de OBSERVACION (2*1)
        

    def H(self,_Xk):
        vector = np.zeros((4,1),)
        vector[0][0] =  math.atan2(_Xk[1][0], _Xk[0][0])  #angullo
        vector[1][0] =  math.sqrt((_Xk[0][0])**2 + (_Xk[1][0])**2) #distancia
        return vector


    def imprimir_resultados(self):
        table = PrettyTable()
        table.field_names = ["x","y","vx","vy"]
        for i in range(0,4):
            table.add_row([ 
                str(self.F[i][0]),str(self.F[i][1]),
                str(self.F[i][2]),str(self.F[i][3])
        ])
        table.add_column("  ", ["","","",""])
        table.add_column("σ", ["σx = "+str(self.σQ[0][0]),"σy = "+str(self.σQ[1][0]),"σvx = "+str(self.σQ[2][0]),"σvy = "+str(self.σQ[3][0])])
        table.add_column("  ", ["","","",""])
        table.add_column("W", ["σx = "+str(self.W[0][0]),"σy = "+str(self.W[1][0]),"σvx = "+str(self.W[2][0]),"σvy = "+str(self.W[3][0])])
        table.add_column("  ", ["","","",""])
        table.add_column("R", ["σx = "+str(self.σR[0][0]),"σy = "+str(self.σR[1][0]),"σvx = ","σvy = "])
        table.add_column("  ", ["","","",""])
        table.add_column("V", ["σx = "+str(self.V[0][0]),"σy = "+str(self.V[1][0]),"σvx = ","σvy = "])
        table.add_column("  ", ["","","",""])
        table.add_column("Xk", ["x = "+str(self.Xk[0][0]),"y = "+str(self.Xk[1][0]),"vx = "+str(self.Xk[2][0]),"vy = "+str(self.Xk[3][0])])
        table.add_column("  ", ["","","",""])
        table.add_column("Zk", ["x = "+str(self.Zk[0][0]),"y = "+str(self.Zk[1][0]),"vx = ","vy = "])
        print(table.get_string(title="Resultados")) 

Pelota()
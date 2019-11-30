from scipy.stats import norm
from prettytable import PrettyTable
import numpy as np
import time
import math

class Filtro():
    def __init__(self,x=3,y=5,Pk1=0.2,Pk2=0.1): #Pk2 = Covarianza
        self.valor_L = 2
        self.valor_λ = (((10**-3)**2)*(self.valor_L + 0)) -self.valor_L #Se puede calcular  asi α**2(L + κ) − L
        self.punto_medio_Xk1 = np.array([[x],[y]])
        self.covarianza_Pk =  np.array([[Pk1,0],[0,Pk2]])
        self.puntos_sigmas_Xk= None
        self.pesos_W = None
        self.puntos_sigmas_Xt = np.array([[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]])
        self.Pk = None
        
        self.puntos_sigma()
        self.prediccion()
        self.actualizacion()
        self.imprimir_resultados()

    def puntos_sigma(self):
        Xk1 = self.punto_medio_Xk1 +  (((self.valor_L+self.valor_λ)*self.covarianza_Pk)**1/2)
        Xk2 = self.punto_medio_Xk1 -  (((self.valor_L+self.valor_λ)*self.covarianza_Pk)**1/2)
        self.puntos_sigmas_Xk = np.concatenate((self.punto_medio_Xk1,Xk1,Xk2),axis=1)
        
        self.pesos_W = (self.valor_λ) / (self.valor_L + self.valor_λ) #(self.valor_λ) / (2 * (self.valor_L + self.valor_λ))
        print((self.valor_λ) / (self.valor_L + self.valor_λ))
        print(((self.valor_λ) / (self.valor_L + self.valor_λ)) + (1 - (10**-3)**2 - 2))
        print(self.pesos_W)
        print(math.atan2(5,3))
        
    def prediccion(self): 
        for j in range(0,(self.valor_L*2 +1)):
            print(math.sqrt((self.puntos_sigmas_Xk[0][j] **2)+(self.puntos_sigmas_Xk[1][j] **2)))
            self.puntos_sigmas_Xt[0][j] =  math.atan2(self.puntos_sigmas_Xk[1][j],self.puntos_sigmas_Xk[0][j]) #y x
            self.puntos_sigmas_Xt[1][j] = math.sqrt((self.puntos_sigmas_Xk[0][j] **2)+(self.puntos_sigmas_Xk[1][j] **2))
        
    def actualizacion(self):
        pass


    def imprimir_resultados(self):
        print("Puntod Medio X:   ",self.punto_medio_Xk1)
        print("Covarianza X:   ",self.covarianza_Pk)
        print("Puntos Sigmas X:   ",self.puntos_sigmas_Xk)
        print("Puntos Sigmas Xt:   ",self.puntos_sigmas_Xt)

Filtro()
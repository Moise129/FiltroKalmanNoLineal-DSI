from prettytable import PrettyTable
import numpy as np
import math
import copy


class Filtro():
    def __init__(self,Xt,σQ , F):
        self.Xˆk = copy.copy(Xt)
        self.σQ = σQ
        
        self.Q = np.array([[σQ[0][0]**2,0,0,0],[0,σQ[1][0]**2,0,0],[0,0,σQ[2][0]**2,0],[0,0,0,σQ[3][0]**2]])
        #np.array([[σQ[0][0],0,0,0],[0,σQ[1][0],0,0],[0,0,σQ[2][0],0],[0,0,0,σQ[3][0]]])
        self.PK = self.Q
        self.R = np.array([[σQ[0][0]**2,0,0,0],[0,σQ[1][0]**2,0,0],[0,0,σQ[2][0]**2,0],[0,0,0,σQ[3][0]**2]])
        self.F = F
        self.predicha= None
        #self.imprimir_resultados()

    # sE APAGO MI CELULAR , AHORITA PRENDE


    def iniciar_proceso(self,Zk):
        #self.Zk = Zk
        Pˆzk_zk = np.zeros((4,4),)
        Pˆxk_zk = np.zeros((4,4),)

        self.Xˆk = np.matmul(self.F,copy.copy(self.Xˆk)) #ᶦ
        self.predicha = np.matmul(self.F,copy.copy(self.Xˆk))

        PˆK = np.matmul(np.matmul(self.F,self.PK),np.transpose(self.F))  + 1
        Xᶦk = np.concatenate(( copy.copy(self.Xˆk), (copy.copy(self.Xˆk) + (PˆK**1/2) )  , (copy.copy(self.Xˆk) - (PˆK**1/2) )),axis=1)

        Zᶦk = self.H(Xᶦk) #+ np.random.normal(0,self.σQ**2)
        Zˆk = (np.mean(Zᶦk , axis=1)).reshape((4,1))
        
        for i in range(0,9):
            Pˆzk_zk = Pˆzk_zk + (np.matmul((Zᶦk[:,i].reshape((4,1))-Zˆk) , np.transpose(Zᶦk[:,i].reshape((4,1)) - Zˆk) ) ) #Ok
            Pˆxk_zk = Pˆxk_zk + ( np.matmul((Xᶦk[:,i].reshape((4,1))- copy.copy(self.Xˆk) ) , np.transpose(Zᶦk[:,i].reshape((4,1)) - Zˆk) ))
        Pˆzk_zk  = Pˆzk_zk * 1/9
        Pˆxk_zk  = Pˆxk_zk * 1/9

        K = np.matmul(Pˆxk_zk, np.linalg.pinv(Pˆzk_zk))
        

        print( np.matmul ( K , np.matmul(Pˆzk_zk, np.transpose(K)) ))
        

        self.Xˆk = copy.copy(self.Xˆk) + np.matmul(K , Zk - Zˆk)
        
        print("Zk      ",Zk)
        print("Z`k     :",Zˆk)
        print("Ganancia:    ",K)
        print("Multiplicar:    ",np.matmul(Pˆzk_zk, np.transpose(K)))
        print("Multiplicar1:    ",( np.matmul ( K , np.matmul(Pˆzk_zk, np.transpose(K)) ) ))
        print("Vector de estado actualizado:    ",self.Xˆk)
        self.PK = PˆK - ( np.matmul ( K , np.matmul(Pˆzk_zk, np.transpose(K)) ) )

    def H(self,Xᶦk):
        vector = np.zeros((4,9),)
        for i in range(0,9):
            vector[0][0] = math.atan2( Xᶦk[1][0],Xᶦk[0][0]) #angulo
            vector[1][0] = math.sqrt((Xᶦk[0][0])**2 + (Xᶦk[1][0])**2)   #distancia
        return vector


    def imprimir_resultados(self):
        table = PrettyTable()
        table.field_names = ["x","y","vx","vy"]
        for i in range(0,4):
            table.add_row([ 
                str(self.F[i][0]),str(self.F[i][1]),
                str(self.F[i][2]),str(self.F[i][3])
        ])
        table.add_column("    ", ["","","",""])
        table.add_column("σ", ["σx = "+str(self.Q[0][0]),"σy = "+str(self.Q[1][0]),"σvx = "+str(self.Q[2][0]),"σvy = "+str(self.Q[3][0])])

        table.add_column("    ", ["","","",""])
        table.add_column("PK", ["σx = "+str(self.PK[0][0]),"σy = "+str(self.PK[1][0]),"σvx = "+str(self.PK[2][0]),"σvy = "+str(self.PK[3][0])])

        table.add_column("  ", ["","","",""])
        table.add_column("Zk (Real)", ["x = "+str(self.Zk[0][0]),"y = "+str(self.Zk[1][0]),"vx = "+str(self.Zk[2][0]),"vy = "+str(self.Zk[3][0])])

        table.add_column("  ", ["","","",""])
        table.add_column("Zk (Predicha)", ["x = "+str(self.X[0][0]),"y = "+str(self.X[1][0]),"vx = "+str(self.X[2][0]),"vy = "+str(self.X[3][0])])


        table.add_column("    ", ["","","",""])
        table.add_column("Xˆk (Estimada)", ["x = "+str(self.Xˆk[0][0]),"y = "+str(self.Xˆk[1][0]),"vx = "+str(self.Xˆk[2][0]),"vy = "+str(self.Xˆk[3][0])])

        print(table.get_string(title="Resultados")) 

#Filtro( np.array([[1],[1],[1],[1]]), np.array([[1],[1],[1],[1]]), np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]]) )
import numpy as np
import matplotlib.pyplot as plt
import random

#Constantes
tablero=[40,20]
x = np.matrix('1.0 10.0 7.0 1.5').T
Dt = 1
F = np.matrix([
    [1, 0, Dt, 0],
    [0, 1, 0, Dt],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
H = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0]
])
gamaE=np.matrix([
    [0.005],
    [0.005],
    [0.004],
    [0.004]
])
Q = gamaE@gamaE.T
Q[0,1]=0
Q[0,2]=0
Q[0,3]=0

Q[1,0]=0
Q[1,2]=0
Q[1,3]=0

Q[2,0]=0
Q[2,1]=0
Q[2,3]=0

Q[3,0]=0
Q[3,1]=0
Q[3,2]=0
gamaO=np.matrix([
    [0.005], 
    [0.005]
])
R=gamaO@gamaO.T
R[0,1]=0
R[1,0]=0
P=Q.copy()
G=np.array([
    [0],
    [0],
    [1],
    [1]
])
#Clases
class Pelota:
    def __init__(self,masa, radio):
        self.masa = masa
        self.radio = radio

class Raqueta:
    def __init__(self,id, ancho, largo, masa, vel_min, vel_max):
        self.id = id
        self.ancho = ancho
        self.largo = largo
        self.masa = masa
        self.vel_min = vel_min
        self.vel_max = vel_max
        
#Funciones
def kalman_xy(Xe, P, Zt):
    #Prediccion
    Xp = F @ Xe
    P = ((F @ P) @ F.T) + Q
    Zp = H @ Xp
    
    #Actualizacion
    y = Zt-Zp
    S = ((H @ P) @ H.T) + R
    S =np.linalg.inv(S)
    K = (P @ H.T) @ S
    I = np.matrix(np.eye((K@H).shape[0]))
    P = (I-(K@H))@P
    x = Xp + (K@y)
    #y = Zt - H * Xe
    #S = H * P * H.T + R  # residual convariance
    #K = P * H.T * np.linalg.pinv(S)    # Kalman gain
    #x = Xe + K*y
    #I = np.matrix(np.eye(F.shape[0])) # identity matrix
    #P = (I - K*H)*P
    # PREDICT x, P based on motion
    #x = F*x
    #P = F*P*F.T + Q
    return x,P

def tiroPelota(xt,G): 
    tiros=[]
    prueba=[]
    for i in range(0,10):
        W = np.matrix(np.random.normal(0, gamaE))
        xt=F@xt+W
        V = np.matrix(np.random.normal(0, gamaO))
        Zt = (H @ xt) + V
        tiros.append(Zt)
        prueba.append([Zt[0,0],Zt[1,0]])
    print("xt: ",prueba)    
    tiros=np.array(tiros)
    prueba=np.array(prueba)
    
    plt.plot(tiros[:,0], tiros[:,1], 'ro')#Grafica real
    #plt.plot(prueba[:,0], prueba[:,1], 'bo')#Grafica real
    return tiros
  
def tiro(P,matrizZt):
    result = []
    W = np.matrix(np.random.normal(0, gamaE))
    prueba=[]
    Xe=np.array([
        [matrizZt[1,0][0]],
        [matrizZt[1,1][0]],
        [(matrizZt[1,0][0]-matrizZt[0,0][0])/Dt],
        [(matrizZt[1,1][0]-matrizZt[0,1][0])/Dt]
    ])
    Xe=Xe+W
    result.append([Xe[0,0],Xe[1,0]])
    for Zt in matrizZt[1:]:
        Xe, P = kalman_xy(Xe.copy(), P,Zt)
        result.append([Xe[0,0],Xe[1,0]])
           
    kalman_x, kalman_y = zip(*result)
    print("Xe: ",result)
    plt.plot(kalman_x,kalman_y, 'go')#Grafica Predicha
    plt.show()

#Velocidad es el arreglo ejemplo v1=[2,4]
#v1 = jugador y v2=pelota
def choqueElastico(m1,v1,m2,v2):
    persona=m1*v1
    movimientoI=persona + m2*v2
    velocidad=(movimientoI-persona)/m2
    return velocidad

#Inicia el programa
matrizZt=tiroPelota(x,G)
tiro(P,matrizZt)
#v=choqueElastico(2,np.array([2,-3]),4,np.array([-3,-3]))
#print("Velocidad que sale la pelota: ",v)
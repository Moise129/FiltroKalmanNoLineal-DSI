from filterpy.kalman import KalmanFilter, MerweScaledSigmaPoints, UnscentedKalmanFilter
from filterpy.common import Q_discrete_white_noise
from numpy import random
from numpy.random import randn
import numpy as np
import matplotlib.pyplot as plt
import math

""" mu, cov, _, _ = kf.batch_filter(zs)
(x, P, K, Pp) = kf.rts_smoother(mu, cov, kf.F, kf.Q)
plt.plot(xs[:, 0], xs[:, 2])
plt.show() """

def fx(x, dt):
    # state transition function - predict next state based
    # on constant velocity model x = vt + x_0
    F = np.array([[1, 0, dt, 0],
                  [0, 1, 0, dt],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]], dtype=float)
    return np.dot(F, x)

def hx(x):
   # measurement function - convert state into a measurement
   # where measurements are [x_pos, y_pos]
    angulo = math.atan2( x[1], x[0] ) #angulo
    distancia = math.sqrt( (x[0])**2 + (x[1])**2 ) #distancia
    return np.array([angulo, distancia])

def inicializar_proceso_real(dt): 
    list_x = []
    list_z = []

    xt = np.matrix('1.0 1.0 1.0 1.0').T    
    F = np.matrix([
        [1, 0, dt, 0],   
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    gamaE=np.matrix([
        [0.005],
        [0.005],
        [0.004],
        [0.004]
    ])
    x_reales = []
    y_reales = []

    for i in range(0,10):
        # Movimiento
        W = np.matrix(np.random.normal(0, gamaE))
        xt = F @ xt + W  # x real
        x = xt[0,0]
        y = xt[1,0]
        print("x:", x, "y:", y)
        list_x.append( [x, y] ) #lista reales
        x_reales.append(x)
        y_reales.append(y)

        # Observacion
        angulo_z = math.atan2( y, x ) #angulo
        distancia_z = math.sqrt( (x)**2 + (y)**2 ) #distancia
        list_z.append( [angulo_z, distancia_z] ) #lista z
    
    plt.plot(x_reales, y_reales, linestyle="-", color='r' )
    
    return list_x, list_z

def iniciar_ukf(list_z):
    dt = 1
    # create sigma points to use in the filter. This is standard for Gaussian processes
    points = MerweScaledSigmaPoints(4, alpha=.1, beta=2., kappa=-1)

    kf = UnscentedKalmanFilter(dim_x=4, dim_z=2, dt=dt, fx=fx, hx=hx, points=points)
    kf.x = np.array([1., 1., 1., 1]) # initial state
    kf.P *= 0.2 # initial uncertainty
    z_std = 0.1
    kf.R = np.diag([z_std**2, z_std**2]) # 1 standard
    kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=0.01**2, block_size=2)

    zs = list_z
    x_predichas = []
    y_predichas = []
    x_estimadas = []
    y_estimadas = []
    for z in zs:
        # Predicción
        kf.predict()
        xp = kf.x[0]
        yp = kf.x[1]
        x_predichas.append(xp)
        y_predichas.append(yp)
        print("PREDICCION: x:", xp, "y:",  yp)
        
        # Actualización
        kf.update(z)
        xe = kf.x[0]
        ye = kf.x[1]
        x_estimadas.append(xe)
        y_estimadas.append(ye)
        print("ESTIMADO: x:", xe, "y:", ye)
        print("--------------------------------------")
    
    plt.plot(x_predichas, y_predichas, linestyle="-", color='orange' )
    plt.plot(x_estimadas, y_estimadas, linestyle="-", color='b' )

    plt.show()

list_x, list_z = inicializar_proceso_real(1)
iniciar_ukf(list_z)
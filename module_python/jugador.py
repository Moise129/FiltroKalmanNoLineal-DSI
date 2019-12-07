import numpy as np
from scipy.stats import norm

class Jugador():
	def __init__(self,matriz_F,vector_x, x,y,vx,vy,vector_sigma,masa_pelota=.5): #sx,sy,svx,svy
		self.masa_pelota = masa_pelota #valor en kg
		self.masa_raqueta = 5 #kg
		self.velocidad_pelota = np.array([vector_x[2][0],vector_x[3][0]])
		self.velocidad_raqueta = np.array([vx,vy])

		self.vector_sigma = vector_sigma  #np.array( [[sx],[sy],[svx],[svy]])
		self.matriz_Q = np.array([
			[self.vector_sigma[0][0]**2,0,0,0],
			[0,self.vector_sigma[1][0]**2,0,0],
			[0,0,self.vector_sigma[2][0]**2,0],
			[0,0,0,self.vector_sigma[3][0]**2]
		])#np.matmul(self.vector_sigma,self.vector_sigma.transpose())

		self.vector_sigma_0 = np.array([[self.vector_sigma[0][0]],[self.vector_sigma[1][0]]])
		self.matriz_R = np.array([
			[self.vector_sigma[0][0]**2,0],
			[0,self.vector_sigma[1][0]**2],
		])

		#np.matmul(self.vector_sigma_0,self.vector_sigma_0.transpose())
		self.matriz_H = np.array([[vector_x[0][0],0,0,0],[0,vector_x[1][0],0,0]])
		self.vector_V = np.array(
			[
                [np.random.normal(0,self.vector_sigma_0[0][0])],
                [np.random.normal(0,self.vector_sigma_0[1][0])]
            ]
		)
		#norm.pdf(self.vector_sigma_0)
		
		movimiento_inicial_p = (self.masa_raqueta * self.velocidad_raqueta) + (self.masa_pelota * self.velocidad_pelota) 
		#movimiento_final_p =  (self.masa_raqueta @ self.velocidad_raqueta) + ( self.masa_pelota @ velocidad_pelota_final) 
		movimiento_final =  (movimiento_inicial_p - (self.masa_raqueta * self.velocidad_raqueta) ) / self.masa_pelota
		print("Movimiento final (Velocidades):  ",movimiento_final)


		self.vector_G = np.array( [[0],[0],[0],[0]]) #np.array( [[0],[0],[movimiento_final[0]],[movimiento_final[1]]]) #cambiara la direccion de la pelota
		self.matriz_F = matriz_F # [X,Y,VX,VY] 
		self.vector_x = vector_x

		self.vector_prediccion_x = np.array( [[x],[y],[vx],[vy]]) #Formula 1  #Formula 7 se actualiza
		self.matriz_confiabilidad = self.matriz_Q #Formula 2    //Inicializamos esta matriz con el valor con la Q     #Formula 8 se actualiza
		self.vector_observacion_prediccion = None  #Formula 3
		self.vector_observacion_real = None #Formula 4
		self.vector_innovacion = None #Formula 5
		self.matriz_ganancia = None #Formula6
		self.proceso()
		#self.imprimir_resultados()


	def proceso(self):
		self.vector_prediccion_x = np.matmul(self.matriz_F,self.vector_prediccion_x) #Formula 1  estado
		self.matriz_confiabilidad = np.matmul(np.matmul(self.matriz_F,self.matriz_confiabilidad), self.matriz_F.transpose()) + self.matriz_Q #Formula 2
		self.vector_observacion_prediccion = np.matmul(self.matriz_H,self.vector_prediccion_x) #+ self.vector_G #Formula 3
		self.vector_observacion_real = np.matmul(self.matriz_H, self.vector_x) + self.vector_V #Formula 4 formula observacion real
		self.vector_innovacion = self.vector_observacion_real - self.vector_observacion_prediccion #Formula5

		part_1 = np.matmul(self.matriz_confiabilidad, self.matriz_H.transpose())
		part_2 = (np.matmul( np.matmul(self.matriz_H,self.matriz_confiabilidad) , self.matriz_H.transpose()) + self.matriz_R) 
		self.matriz_ganancia =  np.matmul( part_1 ,np.linalg.pinv(part_2))

		self.vector_prediccion_x = self.vector_prediccion_x + np.matmul(self.matriz_ganancia, self.vector_innovacion)  #Formula 7  ¿Se actualizo la matriz de prediccion?
		self.matriz_confiabilidad = np.matmul(np.identity(4) - np.matmul(self.matriz_ganancia,self.matriz_H) , self.matriz_confiabilidad ) 		#Formula8


	def imprimir_resultados(self):
		print("Matriz sigma:  ",self.vector_sigma)
		print("Matriz Q:    ",self.matriz_Q)
		print("Matriz Sigma0:    ",self.vector_sigma_0)
		print("Matriz R:   ",self.matriz_R)
		print("Matriz H:     ",self.matriz_H)
		print("Matriz V:     ",self.vector_V)
		print("Matriz G:      ",self.vector_G)
		print("Matriz F:    ",self.matriz_F)
		print("Matriz X:    ",self.vector_x)

		print("Matriz Prediccion:     ",self.vector_prediccion_x)
		print("Matriz Confiabilidad:      ",self.matriz_confiabilidad)
		print("Matriz Observacion prediccion:    ",self.vector_observacion_prediccion)
		print("Matriz Observacion real:    ",self.vector_observacion_real)
		print("Matriz Imnvacion:     ",self.vector_innovacion)
		print("Matriz Ganancia:      ",self.matriz_ganancia)
	
	def imprimir_resultados_importantes(self):
		print("Matriz prediccion:    ",self.vector_prediccion_x)
		print("Matriz Observacion real:    ",self.vector_observacion_real)
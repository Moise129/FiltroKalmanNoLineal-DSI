from tkinter import *
import time
from tkinter import messagebox
import numpy as np

from scipy.stats import norm

import tkinter 
from tkinter import *  
from tkinter import ttk, font

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from prettytable import PrettyTable


from module_python.pelota import Pelota
from module_python.jugador import Jugador
from module_python.filtro import Filtro

class Animacion():
	def __init__(self):
		self.dt = 0.05
		self.pelotita = Pelota(self.dt,1,1,1,1,10,10,20,20) #self,dt,x,y,vx,vy,sx,svx,sy,svy

		self.ventana = Tk()
		self.canvas = Canvas(self.ventana,width=800,height=400)
		self.ventana.geometry("400x400")
		self.canvas.place(x=0,y=0)
		self.boton = Button(self.ventana,command=self.iniciar,text="Iniciar")
		self.boton.place(x=180,y=0)
		self.pelota = self.canvas.create_oval(30,60,50,80,fill='blue')
		self.jugador1 = self.canvas.create_rectangle(0,0,20,100,fill='red')
		self.jugador2 = self.canvas.create_rectangle(380,0,400,100,fill='yellow')
		self.line_middle = self.canvas.create_rectangle(198,0,202,400,fill='white')
		self.ventana.bind("<Key>",self.key)
		self.ventana.mainloop()
		

	def iniciar(self):
		self.boton.place(x=-50,y=-20)
		self.animacion()

	def key(self,event): 

		#Jugador(self.pelotita.matriz_f, self.pelotita.vector_x,0,1,3,5,self.pelotita.vector_sigma)

		if event.keycode==65:
			self.canvas.move(self.jugador1,0,4)
		if event.keycode==81:
			self.canvas.move(self.jugador1,0,-4)
		if event.keycode==40:
			self.canvas.move(self.jugador2,0,4)
		if event.keycode==38:
			self.canvas.move(self.jugador2,0,-4)

	def animacion(self):
		"""x=1
		y=1 """
		while True:
			self.pelotita.obtener_estado(self.pelotita.vector_x)
			coordenadas=self.canvas.coords(self.pelota)
			x=self.colision(self.pelotita.vector_x[2][0]) #valor de vx

			print("valor X: ",x)
			print("Valor Y: ",self.pelotita.vector_x[3][0])
			if x==0:
				messagebox.showinfo("Perdiste","Perdiste jugador rojo")
				self.ventana.destroy()
				obj = Animacion()
			if x==2:
				messagebox.showinfo("Perdiste","Perdiste jugador amarillo")
				self.ventana.destroy()
				obj = Animacion()
			if coordenadas[3]>=400:
				self.pelotita.vy=-1
			if  coordenadas[1]<=0:
				self.pelotita.vy=1
			time.sleep(self.dt)
			x = self.pelotita.vector_x[2][0]
			y = self.pelotita.vector_x[3][0]
			self.canvas.move(self.pelota,x,y)
			self.canvas.update()
			

	def colision(self,x):
		coordenadasJ1 = self.canvas.coords(self.jugador1)
		coordenadasJ2 = self.canvas.coords(self.jugador2)
		coordenadasP = self.canvas.coords(self.pelota)
		print("CordenADAS DE LA PELOTA:   ",coordenadasP)
		time.sleep(0.005)
		if (coordenadasJ1[0]<=coordenadasP[0] and coordenadasJ1[2]>=coordenadasP[0] and coordenadasJ1[1]<=coordenadasP[1] and coordenadasJ1[3]>=coordenadasP[1]) or (coordenadasJ1[0]<=coordenadasP[0] and coordenadasJ1[2]>=coordenadasP[0] and coordenadasJ1[1]<=coordenadasP[3] and coordenadasJ1[3]>=coordenadasP[3]):
			x = 1 #jugador 1 reboto la pelota
			self.pelotita.obtener_estado(self.pelotita.vector_x * -1)
		elif (coordenadasJ2[0]<=coordenadasP[2] and coordenadasJ2[2]>=coordenadasP[2] and coordenadasJ2[1]<=coordenadasP[1] and coordenadasJ2[3]>=coordenadasP[1]) or (coordenadasJ2[0]<=coordenadasP[2] and coordenadasJ2[2]>=coordenadasP[2] and coordenadasJ2[1]<=coordenadasP[3] and coordenadasJ2[3]>=coordenadasP[3]):
			x= -1 #jugador 2 reboto la pelota
			print("pego jugador 2")
			self.pelotita.obtener_estado(self.pelotita.vector_x * -1)
		elif coordenadasP[0]<=10:
			x= 0 #El valon paso al jugador 1
		elif coordenadasP[2]>=390:
			x= 2 #El valon paso al jugador 2
		return x
obj = Animacion()
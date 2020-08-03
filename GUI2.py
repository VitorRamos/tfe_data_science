import pandas as pd
import inspect,os,matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')
from pylab import plot,axis,savefig,show,title
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from tkinter import filedialog, messagebox
from tkinter import *

class Graph:
    """ Class that read the draw the different graphes
        Attributes
            fig - The frame of the graph to draw
            ax1 - The choose of the datas to draw
        Methods
            sliders_on_changed()
            simpleGraphe()
            twoGraphes()"""

    def __init__(self,data,master,choice,heightscr,widthscr):
        """ Create a empty object and initialize attributes."""
        self.__master=master
        self.__test=data
        self.__data=data.getData()
        heightscr=heightscr/120
        widthscr=widthscr/150
        self.__fig1 = Figure( figsize=(widthscr,heightscr),dpi=100)
        self.__fig1.subplots_adjust(bottom=0.25,hspace=0.4)
        self.__canvas=FigureCanvasTkAgg(self.__fig1,master=self.__master)
        self.__data_disp= self.__data
        self.__canvas.get_tk_widget().place(x=400,y=10)
        self.__max=data.getMax(self.__data_disp)
        self.__min=data.getMin(self.__data_disp)
        self.__median=data.getMedian(self.__data_disp)
        self.__mean=data.getMean(self.__data_disp)
        self.__choice=choice
        self.__axesX= ["ipmi_power","total_time"]
        self.__axesY= ["ipmi_energy","ipmi_energy"]
        self.__sliders=[0,0,0]
        temp0=[]
        temp1=[]
        self.sfreq=None
        self.scores=None
        self.sinput=None
        min1_v= np.argmin(self.__data_disp[self.__axesY[0]])
        max1_v= np.argmax(self.__data_disp[self.__axesY[0]])
        min2_v= np.argmin(self.__data_disp[self.__axesY[1]])
        max2_v= np.argmax(self.__data_disp[self.__axesY[1]])
        self.__axis1=self.__fig1.add_subplot(211)
        self.__axis2=self.__fig1.add_subplot(212)
        for i in range (len(self.__data_disp[self.__axesX[0]])):
            temp0.append(self.__median[self.__axesY[0]])
        for i in range (len(self.__data_disp[self.__axesX[1]])):
            temp1.append(self.__median[self.__axesY[1]])
        mean1= self.__data_disp[self.__axesY[0]].mean()
        mean2= self.__data_disp[self.__axesY[1]].mean()
        median2= self.__data_disp[self.__axesY[1]].median()
        median1= self.__data_disp[self.__axesY[0]].median()
        self.__axis1.set_title('Graphe 1')
        self.__axis2.set_title('Graphe 2')
        if self.__choice == 'L':
            markers=[[self.__data_disp.loc[self.__data_disp[self.__axesX[0]]==self.__min[self.__axesX[0]]].index[0]],
                [self.__data_disp.loc[self.__data_disp[self.__axesX[0]]==self.__max[self.__axesX[0]]].index[0]],
                [self.__data_disp.loc[self.__data_disp[self.__axesX[0]]==self.__median[self.__axesX[0]]].index[0]]
                ]
            self.__axis1.plot(self.__data_disp.loc[min1_v][self.__axesX[0]], self.__data_disp.loc[min1_v][self.__axesY[0]], 
                                    c='black', marker = "o",label="Minimum")
            self.__axis1.plot(self.__data_disp.loc[max1_v][self.__axesX[0]], self.__data_disp.loc[max1_v][self.__axesY[0]], 
                                    c='green', marker = "o", label="Maximum")
            self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()], [mean1, mean1], 
                                    c='red',label="Mean")
            self.__axis1.plot(self.__data_disp[self.__axesX[0]], temp0,c='red', marker = "P",label="Median")
            self.__axis1.plot(self.__data_disp[self.__axesX[0]],self.__data_disp[self.__axesY[0]], marker = "x", ls='-')
            self.__axis2.plot(self.__data_disp.loc[min2_v][self.__axesX[1]], self.__data_disp.loc[min2_v][self.__axesY[1]], 
                                    c='black',marker = "o",label="Minimum")
            self.__axis2.plot(self.__data_disp.loc[max2_v][self.__axesX[1]], self.__data_disp.loc[max2_v][self.__axesY[1]], 
                                    c='green',marker = "o",label="Maximum")
            self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()], [mean2, mean2], 
                                c='red',label="Mean")
            self.__axis2.plot(self.__data_disp[self.__axesX[1]], temp1,c='red', marker = "P",label="Median")
            self.__axis2.plot(self.__data_disp[self.__axesX[1]], self.__data_disp[self.__axesY[1]],c='red', marker = "o", ls='-')
        if self.__choice == 'B':    
            N=len(self.__data_disp[self.__axesX[0]])
            N=N+4
            ind = np.arange(N)
            width = 0.35
            self.__axis1.bar(ind,self.__data_disp[self.__axesY[0]],width,tick_label=self.__axesY[0])
            self.__axis1.bar(ind,self.__data_disp.loc[min1_v][self.__axesX[0]],width)
            self.__axis1.bar(ind,self.__data_disp.loc[min1_v][self.__axesY[0]], width, color='black')
            self.__axis1.bar(ind,self.__data_disp.loc[max1_v][self.__axesX[0]], width)
            self.__axis1.bar(ind,self.__data_disp.loc[max1_v][self.__axesY[0]], width, color='green')
            self.__axis1.bar(ind,mean1,width, color='red',tick_label="Mean")
            self.__axis1.bar(ind,temp0,width,color='red',tick_label="Median")
            self.__axis1.bar(ind,self.__data_disp[self.__axesX[0]],width,tick_label=self.__axesX[0])
            self.__axis2.bar(ind,self.__data_disp[self.__axesY[1]], width, tick_label = self.__axesY[1])
            self.__axis2.bar(ind,self.__data_disp.loc[min1_v][self.__axesX[1]],width, tick_label="Minimum")
            self.__axis2.bar(ind,self.__data_disp.loc[min1_v][self.__axesY[1]], width, tick_label="Minimum", color='black')
            self.__axis2.bar(ind,self.__data_disp.loc[max1_v][self.__axesX[1]],width, tick_label="Maximum")
            self.__axis2.bar(ind,self.__data_disp.loc[max1_v][self.__axesY[1]],width, color='green', tick_label="Maximum")
            self.__axis2.bar(ind,mean2,width, color='red',tick_label="Mean")
            self.__axis2.bar(ind, temp1,width,color='red', tick_label="Median")
            self.__axis2.bar(ind,self.__data_disp[self.__axesX[1]],width,tick_label=self.__axesX[1])
        if self.__choice == 'P':
            self.__axis1.scatter(self.__data_disp[self.__axesX[0]],self.__data_disp[self.__axesY[0]], marker = "x")
            self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()],
                                [self.__data_disp.loc[min1_v][self.__axesY[0]],self.__data_disp.loc[min1_v][self.__axesY[0]]], 
                                c='black', marker = "o",label="Minimum")
            self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()],
                                [self.__data_disp.loc[max1_v][self.__axesY[0]],self.__data_disp.loc[max1_v][self.__axesY[0]]],
                                c='green', marker = "o", label="Maximum")
            self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()], [mean1, mean1], 
                                c='red',label="Mean")
            self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()], [median1,median1],
                                c='cyan', marker = "P",label="Median")
            median2= self.__data_disp[self.__axesY[1]].median()
            print("mean2",mean2)
            print("median2",median2)
            self.__axis2.scatter(self.__data_disp[self.__axesX[1]], self.__data_disp[self.__axesY[1]],c='blue', marker = "o")
            self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()],
                                [self.__data_disp.loc[min2_v][self.__axesY[1]], self.__data_disp.loc[min2_v][self.__axesY[1]]], 
                                c='black',marker = "o",label="Minimum")
            self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()],
                                [self.__data_disp.loc[max2_v][self.__axesY[1]],self.__data_disp.loc[max2_v][self.__axesY[1]]],
                                c='green',marker = "o",label="Maximum")
            self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()], [mean2, mean2], 
                                    c='red',label="Mean")
            self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()],
                                [median2, median2],c='cyan', marker = "P",label="Median")
        self.__axis1.set_xlabel(self.__axesX[0])
        self.__axis1.set_ylabel(self.__axesY[0])
        self.__box1 = self.__axis1.get_position()
        self.__pos1=self.__box1.width * 0.7
        self.__axis1.set_position([self.__box1.x0, self.__box1.y0, self.__pos1, self.__box1.height])
        self.__axis1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.__axis2.set_xlabel(self.__axesX[1])
        self.__axis2.set_ylabel(self.__axesY[1])
        self.__box2 = self.__axis2.get_position()
        self.__pos2=self.__box2.width * 0.7
        self.__axis2.set_position([self.__box2.x0, self.__box2.y0, self.__pos2, self.__box2.height])
        self.__axis2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
        #self.__graph=self.simpleGraphe(self.__sliders)
        self.__graph=self.twoGraphes(self.__sliders)

    def sliders_on_changed(self,val):
        """Display a sliding bar controlling a variable.
        :param val: The variable to modify"""
        print('freq',self.sfreq)
        if self.sfreq!=None:
            print(self.__axfreq.get_visible())
        print('input',self.sinput)
        if self.sinput!=None:
            print(self.__axinput.get_visible())
        if self.sfreq!=None:
            self.__freq=self.sfreq.val
        if self.scores!=None:
            self.__core=self.scores.val
        if self.sinput!=None:
            self.__input=self.sinput.val
        if self.sfreq!=None and self.__axfreq.get_visible()==True:
            print('frequence',self.__freq)
            if self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==True and self.__axinput.get_visible()==True:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)
                                                &(self.__data["input"]==self.__input)]
            elif(self.scores!=None and self.sinput==None and self.__axcore.get_visible()==True)or(self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==True and self.__axinput.get_visible()==False):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)]
            elif(self.scores==None and self.sinput!=None and self.__axinput.get_visible()==True)or(self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==False and self.__axinput.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["input"]==self.__input)]
            else:
                self.__data_disp= self.__data_disp[self.__data_disp["frequency"]==self.__freq]
        if self.sinput!=None and self.__axinput.get_visible():
            if self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==True and self.__axfreq.get_visible()==True:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)
                                                &(self.__data["input"]==self.__input)]
            elif(self.sfreq!=None and self.scores==None)or(self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==False and self.__axfreq.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["input"]==self.__input)&(self.__data["frequency"]==self.__freq)]
            elif(self.sfreq==None and self.scores!=None)or(self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==True and self.__axfreq.get_visible()==False):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["input"]==self.__input)]
            else:
                self.__data_disp= self.__data_disp[self.__data_disp["input"]==self.__input]
        if self.scores!=None and self.__axcore.get_visible():
            if(self.sfreq!=None and self.sinput!=None and self.__axfreq.get_visible()==True and self.__axinput.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)
                                                &(self.__data["input"]==self.__input)]
            elif(self.sfreq!=None and self.sinput==None)or(self.sfreq!=None and self.sinput!=None and self.__axfreq.get_visible()==True and self.__input.get_visible()==False):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)]
            elif(self.sfreq==None and self.sinput!=None)or(self.sfreq!=None and self.sinput!=None and self.__axfreq.get_visible()==False and self.__input.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["input"]==self.__input)]
            else:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)]
        self.updateType(self.__choice)

    def simpleGraphe(self,sliders):
        """The graph to draw.
        :param master: The window where to draw the graph.
        :param data: The data to draw."""
        self.__sliders=sliders
        self.__fig1.subplots_adjust(bottom=0.2)
        self.__axcolor = 'lightgoldenrodyellow'
        if self.__sliders[1]==1:
            if self.sfreq==None:
                self.__axfreq=self.__fig1.add_axes([0.2, 0.11, 0.6, 0.03], facecolor=self.__axcolor)
                self.sfreq=Slider(self.__axfreq,'Frequency',self.__min["frequency"],self.__max["frequency"],valinit=self.__min["frequency"]
                    ,valstep=100000)
                self.sfreq.on_changed(self.sliders_on_changed)
            else:
                self.__axfreq.set_visible(True)
        elif self.sfreq:
            self.__axfreq.set_visible(False)
            if self.scores!=None and self.sinput!=None:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["input"]==self.__input)]
            if self.scores!=None and self.sinput==None:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)]
            if self.scores==None and self.sinput!=None:
                self.__data_disp= self.__data[(self.__data["input"]==self.__input)]
            elif self.scores==None and self.sinput==None:
                self.__data_disp= self.__data
        if self.__sliders[0]==1:
            if self.scores==None:
                self.__axcore=self.__fig1.add_axes([0.2, 0.07, 0.6, 0.03], facecolor=self.__axcolor)
                self.scores=Slider(self.__axcore,'Cores',self.__min["cores"],self.__max["cores"], valinit=self.__min["cores"],valstep=1)
                self.scores.on_changed(self.sliders_on_changed)
            else:
                self.__axcore.set_visible(True)
        elif self.scores:
            self.__axcore.set_visible(False)
            if self.sfreq!=None and self.sinput!=None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["input"]==self.__input)]
            if self.sfreq!=None and self.sinput==None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)]
            if self.sfreq==None and self.sinput!=None:
                self.__data_disp= self.__data[(self.__data["input"]==self.__input)]
            elif self.sfreq==None and self.sinput==None:
                self.__data_disp= self.__data
        if self.__sliders[2]==1:
            if self.sinput==None:
                self.__axinput=self.__fig1.add_axes([0.2, 0.03, 0.6, 0.03], facecolor=self.__axcolor)    
                self.sinput=Slider(self.__axinput,'Input',self.__min["input"],self.__max["input"], valinit=self.__min["input"],valstep=1)    
                self.sinput.on_changed(self.sliders_on_changed)
            else:
                self.__axinput.set_visible(True)
        elif self.sinput:
            self.__axinput.set_visible(False)
            if self.sfreq!=None and self.scores!=None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["cores"]==self.__core)]
            if self.sfreq!=None and self.scores==None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)]
            if self.sfreq==None and self.scores!=None:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)]
            elif self.sfreq==None and self.scores==None:
                self.__data_disp= self.__data
        self.updateType(self.__choice)
        self.__canvas.draw()
        
    #@property
    def twoGraphes(self,sliders):
        """Creating to graph to compare them."""
        self.__sliders=sliders
        self.__fig1.subplots_adjust(bottom=0.2,hspace=0.2)
        self.__graphe=plt.subplots(2)
        self.__axcolor = 'lightgoldenrodyellow'
        print(self.__sliders)
        print('freq',self.sfreq)
        print('inp',self.sinput)
        if self.__sliders[1]==1:
            if self.sfreq==None:
                self.__axfreq=self.__fig1.add_axes([0.2,0.11,0.6,0.03], facecolor=self.__axcolor)
                self.sfreq=Slider(self.__axfreq,'Frequency',self.__min["frequency"],self.__max["frequency"],valinit=self.__min["frequency"]
                    ,valstep=100000)
                self.sfreq.on_changed(self.sliders_on_changed)
            else:
                self.__axfreq.set_visible(True)
        elif self.sfreq:
            self.__axfreq.set_visible(False)
            if self.scores!=None and self.sinput!=None:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["input"]==self.__input)]
            if self.scores!=None and self.sinput==None:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)]
            if self.scores==None and self.sinput!=None:
                if self.__input!=None:
                    self.__data_disp= self.__data[(self.__data["input"]==self.__input)]
            elif self.scores==None and self.sinput==None:
                self.__data_disp= self.__data
        if self.__sliders[0]==1:
            if self.scores==None:
                self.__axcore=self.__fig1.add_axes([0.2, 0.07, 0.6, 0.03], facecolor=self.__axcolor)
                self.scores=Slider(self.__axcore,'Cores',self.__min["cores"],self.__max["cores"], valinit=self.__min["cores"],valstep=1)
                self.scores.on_changed(self.sliders_on_changed)
            else:
                self.__axcore.set_visible(True)
        elif self.scores:
            self.__axcore.set_visible(False)
            if self.sfreq!=None and self.sinput!=None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["input"]==self.__input)]
            if self.sfreq!=None and self.sinput==None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)]
            if self.sfreq==None and self.sinput!=None:
                self.__data_disp= self.__data[(self.__data["input"]==self.__input)]
            elif self.sfreq==None and self.sinput==None:
                self.__data_disp= self.__data
        if self.__sliders[2]==1:
            if self.sinput==None:
                self.__axinput=self.__fig1.add_axes([0.2, 0.03, 0.6, 0.03], facecolor=self.__axcolor)    
                self.sinput=Slider(self.__axinput,'Input',self.__min["input"],self.__max["input"], valinit=self.__min["input"],valstep=1)    
                self.sinput.on_changed(self.sliders_on_changed)
            else:
                self.__axinput.set_visible(True)
        elif self.sinput:
            self.__axinput.set_visible(False)
            if self.sfreq!=None and self.scores!=None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["cores"]==self.__core)]
            if self.sfreq!=None and self.scores==None:
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)]
            if self.sfreq==None and self.scores!=None:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)]
            elif self.sfreq==None and self.scores==None:
                self.__data_disp= self.__data
        """self.__fig2.subplots_adjust(bottom=0.2)
        self.__axcolor = 'lightgoldenrodyellow'
        self.__names=['groupa','groupb','groupc']
        self.__values=['1','10','100']
        plot(names,values)
        self.__canvas=FigureCanvasTkAgg(self.__fig)
        self.__canvas.get_tk_widget().place(x=300,y=40)"""
        if self.sfreq!=None:
            print('fr',self.__axfreq.get_visible())
        if self.sinput!=None:
            print('in',self.__axinput.get_visible())
        self.updateType(self.__choice)
        self.__canvas.draw()

    def reset(self):
        self.__choice='P'
        if self.__sliders[0]==1:
            if self.sfreq!=None:
                self.sfreq.reset()
        if self.__sliders[1]==1:
            if self.scores!=None:
                self.scores.reset()
        if self.__sliders[2]==1:
            if self.sinput!=None:
                self.sinput.reset()
        #graphini=self.simpleGraphe([0,0,0])
        graphini=self.twoGraphes([0,0,0])
        self.updateType('P')
       
    def set_axeX(self, val):
        self.__axesX[0]= val

    def set_axeY(self, val):
        self.__axesY[0]= val

    def set_axeX1(self, val):
        print(self.__axesX)
        self.__axesX[1]= val
        print(self.__axesX)

    def set_axeY1(self, val):
        self.__axesY[1]= val
        self.updateType()
        
    def updateType(self,choice):
        self.__axis1.clear()
        self.__axis2.clear()
        self.__choice=choice
        temp0=[]
        temp1=[]
        min1_v= np.argmin(self.__data_disp[self.__axesY[0]])
        max1_v= np.argmax(self.__data_disp[self.__axesY[0]])
        min2_v= np.argmin(self.__data_disp[self.__axesY[1]])
        max2_v= np.argmax(self.__data_disp[self.__axesY[1]])
        print('max',max2_v)
        print('min',min2_v)
        self.__axis1=self.__fig1.add_subplot(211)
        self.__axis2=self.__fig1.add_subplot(212)
        for i in range (len(self.__data_disp[self.__axesX[0]])):
            temp0.append(self.__median[self.__axesY[0]])
        for i in range (len(self.__data_disp[self.__axesX[1]])):
            temp1.append(self.__median[self.__axesY[1]])
        mean1= self.__data_disp[self.__axesY[0]].mean()
        mean2= self.__data_disp[self.__axesY[1]].mean()
        median2= self.__data_disp[self.__axesY[1]].median()
        median1= self.__data_disp[self.__axesY[0]].median()
        self.__axis1.set_title('Graphe 1')
        self.__axis2.set_title('Graphe 2')
        if not self.__data_disp.empty:
            if self.__choice == 'L':
                self.__axis1.plot(self.__data_disp.loc[min1_v][self.__axesX[0]], self.__data_disp.loc[min1_v][self.__axesY[0]], 
                                    c='black', marker = "o",label="Minimum")
                self.__axis1.plot(self.__data_disp.loc[max1_v][self.__axesX[0]], self.__data_disp.loc[max1_v][self.__axesY[0]], 
                                    c='green', marker = "o", label="Maximum")
                self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()], [mean1, mean1], 
                                    c='red',label="Mean")
                self.__axis1.plot(self.__data_disp[self.__axesX[0]], temp0,c='red', marker = "P",label="Median")
                self.__axis1.plot(self.__data_disp[self.__axesX[0]],self.__data_disp[self.__axesY[0]], marker = "x", ls='-')
                self.__axis2.plot(self.__data_disp.loc[min2_v][self.__axesX[1]], self.__data_disp.loc[min2_v][self.__axesY[1]], 
                                    c='black',marker = "o",label="Minimum")
                self.__axis2.plot(self.__data_disp.loc[max2_v][self.__axesX[1]], self.__data_disp.loc[max2_v][self.__axesY[1]], 
                                    c='green',marker = "o",label="Maximum")
                self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()], [mean2, mean2], 
                                c='red',label="Mean")
                self.__axis2.plot(self.__data_disp[self.__axesX[1]], temp1,c='red', marker = "P",label="Median")
                self.__axis2.plot(self.__data_disp[self.__axesX[1]], self.__data_disp[self.__axesY[1]],c='red', marker = "o", ls='-')
            if self.__choice == 'B':    
                N=len(self.__data_disp[self.__axesX[0]])
                N=N+4
                ind = np.arange(N)
                width = 0.35
                self.__axis1.bar(ind,self.__data_disp[self.__axesY[0]],width,tick_label=self.__axesY[0])
                self.__axis1.bar(ind,self.__data_disp.loc[min1_v][self.__axesX[0]],width)
                self.__axis1.bar(ind,self.__data_disp.loc[min1_v][self.__axesY[0]], width, color='black')
                self.__axis1.bar(ind,self.__data_disp.loc[max1_v][self.__axesX[0]], width)
                self.__axis1.bar(ind,self.__data_disp.loc[max1_v][self.__axesY[0]], width, color='green')
                self.__axis1.bar(ind,mean1,width, color='red',tick_label="Mean")
                self.__axis1.bar(ind,temp0,width,color='red',tick_label="Median")
                self.__axis1.bar(ind,self.__data_disp[self.__axesX[0]],width,tick_label=self.__axesX[0])
                self.__axis2.bar(ind,self.__data_disp[self.__axesY[1]], width, tick_label = self.__axesY[1])
                self.__axis2.bar(ind,self.__data_disp.loc[min1_v][self.__axesX[1]],width, tick_label="Minimum")
                self.__axis2.bar(ind,self.__data_disp.loc[min1_v][self.__axesY[1]], width, tick_label="Minimum", color='black')
                self.__axis2.bar(ind,self.__data_disp.loc[max1_v][self.__axesX[1]],width, tick_label="Maximum")
                self.__axis2.bar(ind,self.__data_disp.loc[max1_v][self.__axesY[1]],width, color='green', tick_label="Maximum")
                self.__axis2.bar(ind,mean2,width, color='red',tick_label="Mean")
                self.__axis2.bar(ind, temp1,width,color='red', tick_label="Median")
                self.__axis2.bar(ind,self.__data_disp[self.__axesX[1]],width,tick_label=self.__axesX[1])
            if self.__choice == 'P':
                self.__axis1.scatter(self.__data_disp[self.__axesX[0]],self.__data_disp[self.__axesY[0]], marker = "x")
                self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()], 
                                    [self.__data_disp.loc[min1_v][self.__axesY[0]],self.__data_disp.loc[min1_v][self.__axesY[0]]], 
                                        c='black', marker = "o",label="Minimum")
                self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()], 
                                    [self.__data_disp.loc[max1_v][self.__axesY[0]],self.__data_disp.loc[max1_v][self.__axesY[0]]], 
                                        c='green', marker = "o", label="Maximum")
                self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()],[mean1, mean1], 
                                    c='red',label="Mean")
                self.__axis1.plot([self.__data_disp[self.__axesX[0]].min(), self.__data_disp[self.__axesX[0]].max()], [median1,median1],
                                    c='cyan', marker = "P",label="Median")
                print("mean2",mean2)
                print('median2',median2)
                self.__axis2.scatter(self.__data_disp[self.__axesX[1]], self.__data_disp[self.__axesY[1]],c='blue', marker = "o")
                self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()],
                                    [self.__data_disp.loc[min2_v][self.__axesY[1]],self.__data_disp.loc[min2_v][self.__axesY[1]]],
                                    c='black',marker = "o",label="Minimum")
                self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()],
                                    [self.__data_disp.loc[max2_v][self.__axesY[1]],self.__data_disp.loc[max2_v][self.__axesY[1]]],
                                    c='green',marker = "o",label="Maximum")
                self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()], [mean2, mean2], 
                                        c='red',label="Mean")
                self.__axis2.plot([self.__data_disp[self.__axesX[1]].min(), self.__data_disp[self.__axesX[1]].max()],
                                    [median2, median2],c='cyan', marker = "P",label="Median")
            self.__axis1.set_xlabel(self.__axesX[0])
            self.__axis1.set_ylabel(self.__axesY[0])
            #box1 = self.__axis1.get_position()
            self.__axis1.set_position([self.__box1.x0, self.__box1.y0, self.__pos1, self.__box1.height])
            self.__axis1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            self.__axis2.set_xlabel(self.__axesX[1])
            self.__axis2.set_ylabel(self.__axesY[1])
            #box2 = self.__axis2.get_position()
            self.__axis2.set_position([self.__box2.x0, self.__box2.y0, self.__pos2, self.__box2.height])
            self.__axis2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.__a=self.__fig1.canvas.draw_idle()
    
    def getGraph(self):
        return self.__fig1

    def getVal(self):
        if self.sfreq!=None:
            if self.scores!=None and self.sinput!=None:
                listVal=[self.__freq,self.__input,self.__core]
            if self.scores!=None and self.sinput==None:
                listVal=[self.__freq,self.__input,'None']
            if self.scores==None and self.sinput!=None:
                listVal=[self.__freq,'None',self.__core]
            if self.scores==None and self.sinput==None and self.__axfreq.get_visible()==True:
                listVal=[self.__freq,'None','None']
            else:
                listVal=['None','None','None']
        if self.scores!=None and self.sfreq==None:
            if self.sinput!=None:
                listVal=['None',self.__input,self.__core]
            elif self.__axcore.get_visible()==False:
                listVal=['None','None','None']
            else:
                listVal=['None','None',self.__core]
        if self.sinput!=None and self.sfreq==None:
            if self.scores==None:
                listVal=['None',self.__input,'None']
        if self.sinput==None and self.scores==None and self.sfreq==None:
            listVal=['None','None','None']
        return listVal

class MainWindow:
    """ Class that read the setup file
        Attributes
            setup - The 
            graphe - The frame containing the graph
        Methods
            initGUI()
            graphes()
            MenuBar()
            quit()
            ok()"""

    def __init__(self,master,setup,datas,data,conf,saveGraph,name):
        """ Create a empty object and initialize attributes and GUI with graphe and initGUI methods.
        :param data: Data to draw"""
        self.__confi=conf
        self.__data_read=conf
        self.__setup=setup
        self.__master=master
        self.__max=datas.getMax(data)
        self.__min=datas.getMin(data)
        self.__median=datas.getMedian(data)
        self.__mean=datas.getMean(data)
        self.__saveGraph=saveGraph
        self.__name=name
        self.datas=data
        self.__axes=['ipmi_power','ipmi_energy']
        self.__mask=[0,0,0]
        self.__label_2=None
        self.__label_3=None
        self.__label_4=None
        self.__label_5=None
        self.__label_6=None
        self.__label_7=None
        self.__label_8=None
        self.__label_9=None
        self.__label_10=None
        self.__tkvar=StringVar()
        self.__tkvar1=StringVar()
        self.__tkvar2=StringVar()
        self.__tkvar3=StringVar()
        self.__tkvar4=StringVar()
        self.__choice='C'
        self.initGUI(datas)
        
    def close_window(self):
        global running
        running = False
    
    def initGUI(self,data):
        """Creation of the different object.
        :param data: Data to display"""
        self.__master.protocol("WM_DELETE_WINDOW", self.close_window())
        self.__RWidth=self.__master.winfo_screenwidth()
        self.__RHeight=self.__master.winfo_screenheight()
        self.__master.geometry(str(self.__RWidth)+"x"+str(self.__RHeight))
        self.__master.title('Test')
        self.__master.configure(bg=self.__setup.colorframe)
        self.MenuBar()
        choice=self.typeGraph()
        self.__graphe=Graph(data,self.__master,'P',self.__RHeight,self.__RWidth)
        self.graphes(data.getData())
        self.__closebutton = Button(self.__master, text='X', command=self.quit)
        
    def graphes(self,data):
        """Creation of the graph.
        :param data: Data to draw"""
        var=[]
        self.__label_1=Label(self.__master,text='VARIABLES LIST',justify=LEFT).pack(expand=0,anchor='w')
        for i in range (len(self.__confi["data_descriptor"])):
            vartemp=BooleanVar()
            var.append(vartemp)
            self.__mask.append(0)
            self.__checkbutton_1=Checkbutton(self.__master,text=self.__confi["data_descriptor"]["keys"][i],
                variable=lambda index=i:var[index],onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',justify='left',
                command=lambda index=i:self.update_text(var,index)).pack(expand=0,anchor='w')
        self.choiceAxesX()
        self.choiceAxesY()
        
    def update_text(self,var,i):
        if i==0:
            if self.__label_2==None:
                self.__mask[0]=1
                self.__label_2=Label(self.__master,text='Cores',justify=LEFT)
                self.__label_2.place(x=10,y=450)
                self.__label_3=Label(self.__master,text='Minimum : '+str(self.__min["cores"]),justify=LEFT)
                self.__label_3.place(x=10,y=470)
                self.__label_4=Label(self.__master,text='Maximum : '+str(self.__max["cores"]),justify=LEFT)
                self.__label_4.place(x=10,y=490)
            else:
                self.__mask[0]=0
                self.__label_2.destroy()
                self.__label_3.place_forget()
                self.__label_4.place_forget()
                self.__label_2=None
        if i==1:
            if self.__label_5==None:
                self.__mask[1]=1
                self.__label_5=Label(self.__master,text='Frequency',justify=LEFT)
                self.__label_5.place(x=10,y=510)
                self.__label_6=Label(self.__master,text='Minimum : '+str(self.__min["frequency"]),justify=LEFT)
                self.__label_6.place(x=10,y=530)
                self.__label_7=Label(self.__master,text='Maximum : '+str(self.__max["frequency"]),justify=LEFT)
                self.__label_7.place(x=10,y=550)
            else:
                self.__mask[1]=0
                self.__label_5.destroy()
                self.__label_6.place_forget()
                self.__label_7.place_forget()
                self.__label_5=None
        if i==2:        
            if self.__label_8==None:
                self.__mask[2]=1
                self.__label_8=Label(self.__master,text='Input',justify=LEFT)
                self.__label_8.place(x=10,y=570)
                self.__label_9=Label(self.__master,text='Minimum : '+str(self.__min["input"]),justify=LEFT)
                self.__label_9.place(x=10,y=590)
                self.__label_10=Label(self.__master,text='Maximum : '+str(self.__max["input"]),justify=LEFT)
                self.__label_10.place(x=10,y=610)
            else:
                self.__mask[2]=0
                self.__label_8.destroy()
                self.__label_9.place_forget()
                self.__label_10.place_forget()
                self.__label_8=None
        if i==3:
            for a in range (len(self.__mask)):
                self.__mask[a]=0
            if self.__label_8!=None:
                self.__label_8.destroy()
                self.__label_8=None
            if self.__label_9!=None:
                self.__label_9.place_forget()
            if self.__label_10!=None:
                self.__label_10.place_forget()
            if self.__label_5!=None:
                self.__label_5.destroy()
                self.__label_5=None
            if self.__label_6!=None:
                self.__label_6.place_forget()
            if self.__label_7!=None:
                self.__label_7.place_forget()
            if self.__label_2!=None:
                self.__label_2.destroy()
                self.__label_2=None
            if self.__label_3!=None:
                self.__label_3.place_forget()
            if self.__label_4!=None:
                self.__label_4.place_forget()
        #self.__graphe.simpleGraphe(self.__mask)
        self.__graphe.twoGraphes(self.__mask)
                                    
    def MenuBar(self):
        """This method is called by the initialisation of the interface to 
        create a bar with the different menu."""
        self.__menu = Menu(self.__master)
        self.__master.config(menu=self.__menu)
        #create the different menu.
        self.__filemenu = Menu(self.__menu)
        self.__howtomenu=Menu(self.__menu)
        self.__var9=IntVar()
        self.__var10=IntVar()
        self.__var11=IntVar()
        self.__var12=IntVar()
        self.__var13=IntVar()
        self.__menu.add_cascade(label="Menu", menu=self.__filemenu)
        self.__menu.add_cascade(label="Information", menu=self.__howtomenu)
        #create the different option for the menus.
        self.__howtomenu.add_command(label="Help", command=self.how_to)
        self.__howtomenu.add_command(label='Loading files', command=self.load_file)
        self.__howtomenu.add_command(label="aa")      
        self.__filemenu.add_command(label="Reset", command=self.reset)
        self.__filemenu.add_command(label="Save",command=self.save)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Two graphs", command=self.two)
        self.__filemenu.add_command(label="One graph", command=self.one)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Exit", command=self.quit)
    
    def reset(self):
        self.__graphe.reset()
        self.update_text(None,3)
        self.uncheckall(4,self.__cbs)

    def quit(self):
        """This method is called by the pushing on the 'Exit' menu to close the
        software."""
        if messagebox.askyesno('Verify', 'Do you really to quit?'):
            sys.exit()
    
    def ok(self):
        """This method is called by the 'quit' method to close the main window."""
        self.__master.withdraw()

    def how_to(self):
        """This method is called by the pushing on the 'Help' menu to display in
        a pop_up window the help to use the software."""
        #create the new window with the 'Manual Book' title.
        self.__newWindow = Toplevel(self.__master)
        self.__master=self.__newWindow
        self.__master.title('Manual Book')
        self.__master.geometry("700x430+10+10")
        #display the text
        self.__label_20=Label(self.__master,text="Help: text to write").place(x=215,y=15,width=300,height=25)

    def load_file(self):
        """This method is called by the pushing on the 'Loading file' menu to 
        upload the right result file for the session."""
        #read the session file thanks to the object session.
        self.__name= filedialog.askopenfilename()
        self.datas=data.resu
        return self.__name

    def uncheckall(self,checktest,cbs):
        i=1
        for cb in cbs:
            if i == checktest:
                cb.select()
            else:
                cb.deselect()
            i=i+1
        if checktest == 2 :
            self.__choice = 'B'
        else :
            if checktest == 3 :
                self.__choice = 'P'
            else:
                self.__choice = 'L'
        self.updateGraph()

    def updateGraph(self):
        self.__graphe.updateType(self.__choice)
    
    def change_dropdownType(self,*args):
        if (self.__tkvar.get())=='Lignes':
            self.__choice='L'
        else:
            if (self.__tkvar.get())=='Bars':
                self.__choice='B'
            else:
                self.__choice='P'
        self.updateGraph()

    def typeGraph(self):
        var1=BooleanVar()
        var2=BooleanVar()
        var3=BooleanVar()
        self.__checkbutton_10=Checkbutton(self.__master,text='Lignes',variable=var1,onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',
                command=lambda:self.uncheckall(1,cbs),justify='left')
        self.__checkbutton_11=Checkbutton(self.__master,text='Bars',variable=var2,onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',
                command=lambda:self.uncheckall(2,cbs),justify='left')
        self.__checkbutton_12=Checkbutton(self.__master,text='Points',variable=var3,onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',
                command=lambda:self.uncheckall(3,cbs),justify='left')
        cbs = [self.__checkbutton_10, self.__checkbutton_11, self.__checkbutton_12]
        self.__cbs=cbs
        choices={'Lignes','Bars','Points'}
        self.__tkvar.set('Points')
        popupMenu=OptionMenu(self.__master,self.__tkvar,*choices)
        Label(self.__master,text="Choose a type of graph").pack(expand=0,anchor='w')
        popupMenu.pack(expand=0,anchor='w')
        self.__tkvar.trace('w',self.change_dropdownType)

    def choiceAxesY(self):
        listAxesY=[]
        for i in range (len(self.__confi["data_descriptor"])):
            listAxesY.append(self.__confi["data_descriptor"]["keys"][i])
        print("3",self.__confi["data_descriptor"]["values"])
        listAxesY.append("ipmi_energy")
        listAxesY.append("ipmi_power")
        listAxesY.append("total_time")#self.__confi["data_descriptor"]["values"]
        self.__tkvar2.set('ipmi_energy')
        self.__tkvar3.set('ipmi_energy')
        popupMenu1=OptionMenu(self.__master,self.__tkvar2,*listAxesY)
        Label(self.__master,text='Axe Y Graphe 1:',justify=LEFT).pack(expand=0,anchor='w')
        popupMenu1.pack(expand=0,anchor='w')
        self.__tkvar2.trace('w',self.change_dropdownAxesY)
        popupMenu2=OptionMenu(self.__master,self.__tkvar3,*listAxesY)
        Label(self.__master,text='Axe Y Graphe 2:',justify=LEFT).pack(expand=0,anchor='w')
        popupMenu2.pack(expand=0,anchor='w')
        self.__tkvar3.trace('w',self.change_dropdownAxesY1)
        
    def choiceAxesX(self):
        listAxes=[]
        for i in range (len(self.__confi["data_descriptor"])):
            listAxes.append(self.__confi["data_descriptor"]["keys"][i])
        listAxes.append("total_time")#self.__confi["data_descriptor"]["values"]
        listAxes.append("ipmi_energy")
        listAxes.append("ipmi_power")
        self.__tkvar1.set('ipmi_power')
        self.__tkvar4.set('total_time')
        popupMenu=OptionMenu(self.__master,self.__tkvar1,*listAxes)
        Label(self.__master,text='Axe X:',justify=LEFT).pack(expand=0,anchor='w')
        popupMenu.pack(expand=0,anchor='w')
        self.__tkvar1.trace('w',self.change_dropdownAxesX)
        popupMenu1=OptionMenu(self.__master,self.__tkvar4,*listAxes)
        Label(self.__master,text='Axe X Graphe 2:',justify=LEFT).pack(expand=0,anchor='w')
        popupMenu1.pack(expand=0,anchor='w')
        self.__tkvar4.trace('w',self.change_dropdownAxesX1)

    def change_dropdownAxesX(self,*args):
        print('AxesX')
        self.__graphe.set_axeX(self.__tkvar1.get())
        self.updateGraph()

    def change_dropdownAxesY(self,*args):
        self.__graphe.set_axeY(self.__tkvar2.get())
        self.updateGraph()
    
    def change_dropdownAxesX1(self,*args):
        self.__graphe.set_axeX1(self.__tkvar4.get())
        self.updateGraph()

    def change_dropdownAxesY1(self,*args):
        self.__graphe.set_axeY1(self.__tkvar3.get())
        self.updateGraph()
    
    def save(self):
        name=self.__name.split("\\")
        temp=name[6].replace('completo_',' ')
        graph=self.__graphe.getGraph()
        listeval=self.__graphe.getVal()
        text=''' '''
        self.__saveGraph.saveJson(temp,self.datas,self.__tkvar1.get(),self.__tkvar4.get(),self.__tkvar2.get(),self.__tkvar3.get())
        for i in range(len(self.__confi["data_descriptor"])):
            print(self.__confi["data_descriptor"]["keys"][i])
            text = text+'''Filter on '''+self.__confi["data_descriptor"]["keys"][i]+''':'''+str(listeval[i])
        print(text)
        graph.text(.1,.1,text)
        self.__saveGraph.savePDF(temp,graph,self.__tkvar1.get(),self.__tkvar4.get(),self.__tkvar2.get(),self.__tkvar3.get())

    def two(self):
        print("Two graphs")

    def one(self):
        print("One graph")
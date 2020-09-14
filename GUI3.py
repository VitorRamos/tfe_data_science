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

class Graph1:
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
        widthscr=widthscr/180
        self.__fig = Figure(figsize=(widthscr,heightscr), dpi=100)
        self.__fig.subplots_adjust(bottom=0.25,hspace=0.4)
        self.__canvas=FigureCanvasTkAgg(self.__fig,master=self.__master)
        self.__data_disp= self.__data
        self.__canvas.get_tk_widget().place(x=650,y=10)
        self.__max=data.getMax(self.__data_disp)
        self.__min=data.getMin(self.__data_disp)
        self.__median=data.getMedian(self.__data_disp)
        self.__mean=data.getMean(self.__data_disp)
        self.__choice=choice
        self.__axesX= "ipmi_power"
        self.__axesY= "ipmi_energy"
        self.__sliders=[0,0,0]
        temp=[]
        self.sfreq=None
        self.scores=None
        self.sinput=None
        min_v= np.argmin(self.__data_disp[self.__axesY])
        max_v= np.argmax(self.__data_disp[self.__axesY])
        mean= self.__data_disp[self.__axesY].mean()
        median= self.__data_disp[self.__axesY].median()
        for i in range (len(self.__data_disp[self.__axesX])):
            temp.append(self.__median[self.__axesY])
        self.__axis= self.__fig.add_subplot(111)
        if self.__choice == 'L':
            markers=[[self.__data_disp.loc[self.__data_disp[self.__axesX]==self.__min[self.__axesX]].index[0]],
                [self.__data_disp.loc[self.__data_disp[self.__axesX]==self.__max[self.__axesX]].index[0]],
                [self.__data_disp.loc[self.__data_disp[self.__axesX]==self.__median[self.__axesX]].index[0]]
                ]
            self.__axis.plot(self.__data_disp.loc[min_v][self.__axesX], self.__data_disp.loc[min_v][self.__axesY], 
                                    c='black', marker = "o",label="Minimum")
            self.__axis.plot(self.__data_disp.loc[max_v][self.__axesX], self.__data_disp.loc[max_v][self.__axesY], 
                                    c='green', marker = "o", label="Maximum")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [mean, mean], 
                                    c='red',label="Mean")
            self.__axis.plot(self.__data_disp[self.__axesX], temp,c='red', marker = "P",label="Median")
            self.__axis.plot(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x", ls='-')
        if self.__choice == 'B':    
            N=len(self.__data_disp[self.__axesX])
            #N=N+4
            ind = np.arange(N)
            width = 0.35
            self.__axis.bar(ind,self.__data_disp[self.__axesY],width,tick_label=self.__axesY)
            self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesX],width)
            self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesY], width, color='black')
            self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesX], width)
            self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesY], width, color='green')
            self.__axis.bar(ind,mean,width, color='red',tick_label="Mean")
            self.__axis.bar(ind,temp,width,color='red',tick_label="Median")
            self.__axis.bar(ind,self.__data_disp[self.__axesX],width,tick_label=self.__axesX)
        if self.__choice == 'P':
            self.__axis.scatter(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()],
                                [self.__data_disp.loc[min_v][self.__axesY],self.__data_disp.loc[min_v][self.__axesY]], 
                                c='black', marker = "o",label="Minimum")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()],
                                [self.__data_disp.loc[max_v][self.__axesY],self.__data_disp.loc[max_v][self.__axesY]],
                                c='green', marker = "o", label="Maximum")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [mean, mean], 
                                c='red',label="Mean")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [median,median],
                                c='cyan', marker = "P",label="Median")
        self.__axis.set_xlabel(self.__axesX)
        self.__axis.set_ylabel(self.__axesY)
        self.__box = self.__axis.get_position()
        self.__pos=self.__box.width * 0.7
        self.__axis.set_position([self.__box.x0, self.__box.y0, self.__pos, self.__box.height])
        self.__axis.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
        #self.__graph=self.simpleGraphe(self.__sliders)
        print('sliders',self.__sliders)#
        self.__graph=self.twoGraphes(self.__sliders)

    def sliders_on_changed(self,val):
        """Display a sliding bar controlling a variable.
        :param val: The variable to modify"""
        if self.sfreq!=None:
            self.__freq=self.sfreq.val
        if self.scores!=None:
            self.__core=self.scores.val
        if self.sinput!=None:
            self.__input=self.sinput.val
        if self.sfreq!=None and self.__axfreq.get_visible()==True:
            print('frequence',self.__freq)
            print('axfreq',self.__axfreq.get_visible())
            if self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==True and self.__axinput.get_visible()==True:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)
                                                &(self.__data["input"]==self.__input)]
            elif(self.scores!=None and self.sinput==None and self.__axcore.get_visible()==True)or(self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==True and self.__axinput.get_visible()==False):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)]
            elif(self.scores==None and self.sinput!=None and self.__axinput.get_visible()==True)or(self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==False and self.__axinput.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["input"]==self.__input)]
            else:
                self.__data_disp= self.__data[self.__data["frequency"]==self.__freq]
        if self.sinput!=None and self.__axinput.get_visible():
            print('axinput',self.__axinput.get_visible())
            if self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==True and self.__axfreq.get_visible()==True:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)
                                                &(self.__data["input"]==self.__input)]
            elif(self.sfreq!=None and self.scores==None)or(self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==False and self.__axfreq.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["input"]==self.__input)&(self.__data["frequency"]==self.__freq)]
            elif(self.sfreq==None and self.scores!=None)or(self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==True and self.__axfreq.get_visible()==False):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["input"]==self.__input)]
            else:
                self.__data_disp= self.__data[self.__data["input"]==self.__input]
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
        self.__fig.subplots_adjust(bottom=0.2)
        self.__axcolor = 'lightgoldenrodyellow'
        if self.__sliders[1]==1:
            if self.sfreq==None:
                self.__axfreq=self.__fig.add_axes([0.2, 0.11, 0.6, 0.03], facecolor=self.__axcolor)
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
                self.__axcore=self.__fig.add_axes([0.2, 0.07, 0.6, 0.03], facecolor=self.__axcolor)
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
                self.__axinput=self.__fig.add_axes([0.2, 0.03, 0.6, 0.03], facecolor=self.__axcolor)    
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
        self.__fig.subplots_adjust(bottom=0.2)
        self.__graphe=plt.subplots(111)
        self.__axcolor = 'lightgoldenrodyellow'
        if self.__sliders[1]==1:
            if self.sfreq==None:
                self.__axfreq=self.__fig.add_axes([0.2,0.11,0.6,0.03], facecolor=self.__axcolor)
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
                self.__axcore=self.__fig.add_axes([0.2, 0.07, 0.6, 0.03], facecolor=self.__axcolor)
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
                self.__axinput=self.__fig.add_axes([0.2, 0.03, 0.6, 0.03], facecolor=self.__axcolor)    
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
        """self.__graphe2=plt.subplots(132)
        self.__fig2.subplots_adjust(bottom=0.2)
        self.__axcolor = 'lightgoldenrodyellow'
        self.__names=['groupa','groupb','groupc']
        self.__values=['1','10','100']
        plot(names,values)
        self.__canvas=FigureCanvasTkAgg(self.__fig)
        self.__canvas.get_tk_widget().place(x=300,y=40)"""
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
        self.__axesX= val
        #self.updateType(self.__choice)

    def set_axeY(self, val):
        self.__axesY= val
        
    def updateType(self,choice):
    
        self.__axis.clear()
        self.__choice=choice
        temp=[]
        print('data_disp[self.__axesY]',self.__data_disp[self.__axesY])
        min_v= np.argmin(self.__data_disp[self.__axesY])
        max_v= np.argmax(self.__data_disp[self.__axesY])
        self.__axis=self.__fig.add_subplot(111)
        for i in range (len(self.__data_disp[self.__axesX])):
            temp.append(self.__median[self.__axesY])
        mean= self.__data_disp[self.__axesY].mean()
        median= self.__data_disp[self.__axesY].median()
        self.__axis.set_title('Graphe')
        if not self.__data_disp.empty:
            if self.__choice == 'L':
                self.__axis.plot(self.__data_disp.loc[min_v][self.__axesX], self.__data_disp.loc[min_v][self.__axesY], 
                                    c='black', marker = "o",label="Minimum")
                self.__axis.plot(self.__data_disp.loc[max_v][self.__axesX], self.__data_disp.loc[max_v][self.__axesY], 
                                    c='green', marker = "o", label="Maximum")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [mean, mean], 
                                    c='red',label="Mean")
                self.__axis.plot(self.__data_disp[self.__axesX], temp,c='red', marker = "P",label="Median")
                self.__axis.plot(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x", ls='-')
            if self.__choice == 'B':    
                N=len(self.__data_disp[self.__axesX])
                #N=N+4
                ind = np.arange(N)
                width = 0.35
                self.__axis.bar(ind,self.__data_disp[self.__axesY],width,tick_label=self.__axesY)
                self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesX],width)
                self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesY], width, color='black')
                self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesX], width)
                self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesY], width, color='green')
                self.__axis.bar(ind,mean,width, color='red',tick_label="Mean")
                self.__axis.bar(ind,temp,width,color='red',tick_label="Median")
                self.__axis.bar(ind,self.__data_disp[self.__axesX],width,tick_label=self.__axesX)
            if self.__choice == 'P':
                self.__axis.scatter(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], 
                                    [self.__data_disp.loc[min_v][self.__axesY],self.__data_disp.loc[min_v][self.__axesY]], 
                                        c='black', marker = "o",label="Minimum")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], 
                                    [self.__data_disp.loc[max_v][self.__axesY],self.__data_disp.loc[max_v][self.__axesY]], 
                                        c='green', marker = "o", label="Maximum")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()],[mean, mean], 
                                        c='red',label="Mean")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [median,median],
                                        c='cyan', marker = "P",label="Median")
            self.__axis.set_xlabel(self.__axesX)
            self.__axis.set_ylabel(self.__axesY)
            self.__axis.set_position([self.__box.x0, self.__box.y0, self.__pos, self.__box.height])
            self.__axis.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.__a=self.__fig.canvas.draw_idle()

    def getGraph(self):
        return self.__fig

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

class Graph2:
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
        widthscr=widthscr/180
        self.__fig1 = Figure(figsize=(widthscr,heightscr), dpi=100)
        self.__fig1.subplots_adjust(bottom=0.25,hspace=0.4)
        self.__canvas=FigureCanvasTkAgg(self.__fig1,master=self.__master)
        self.__data_disp= self.__data
        self.__canvas.get_tk_widget().place(x=650,y=500)
        self.__max=data.getMax(self.__data_disp)
        self.__min=data.getMin(self.__data_disp)
        self.__median=data.getMedian(self.__data_disp)
        self.__mean=data.getMean(self.__data_disp)
        self.__choice=choice
        self.__axesX= "ipmi_power"
        self.__axesY= "ipmi_energy"
        self.__sliders=[0,0,0]
        temp=[]
        self.sfreq=None
        self.scores=None
        self.sinput=None
        min_v= np.argmin(self.__data_disp[self.__axesY])
        max_v= np.argmax(self.__data_disp[self.__axesY])
        mean= self.__data_disp[self.__axesY].mean()
        median= self.__data_disp[self.__axesY].median()
        for i in range (len(self.__data_disp[self.__axesX])):
            temp.append(self.__median[self.__axesY])
        self.__axis= self.__fig1.add_subplot(111)
        if self.__choice == 'L':
            markers=[[self.__data_disp.loc[self.__data_disp[self.__axesX]==self.__min[self.__axesX]].index[0]],
                [self.__data_disp.loc[self.__data_disp[self.__axesX]==self.__max[self.__axesX]].index[0]],
                [self.__data_disp.loc[self.__data_disp[self.__axesX]==self.__median[self.__axesX]].index[0]]
                ]
            self.__axis.plot(self.__data_disp.loc[min_v][self.__axesX], self.__data_disp.loc[min_v][self.__axesY], 
                                    c='black', marker = "o",label="Minimum")
            self.__axis.plot(self.__data_disp.loc[max_v][self.__axesX], self.__data_disp.loc[max_v][self.__axesY], 
                                    c='green', marker = "o", label="Maximum")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [mean, mean], 
                                    c='red',label="Mean")
            self.__axis.plot(self.__data_disp[self.__axesX], temp,c='red', marker = "P",label="Median")
            self.__axis.plot(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x", ls='-')
        if self.__choice == 'B':    
            N=len(self.__data_disp[self.__axesX])
            #N=N+4
            ind = np.arange(N)
            width = 0.35
            self.__axis.bar(ind,self.__data_disp[self.__axesY],width,tick_label=self.__axesY)
            self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesX],width)
            self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesY], width, color='black')
            self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesX], width)
            self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesY], width, color='green')
            self.__axis.bar(ind,mean,width, color='red',tick_label="Mean")
            self.__axis.bar(ind,temp,width,color='red',tick_label="Median")
            self.__axis.bar(ind,self.__data_disp[self.__axesX],width,tick_label=self.__axesX)
        if self.__choice == 'P':
            self.__axis.scatter(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()],
                                [self.__data_disp.loc[min_v][self.__axesY],self.__data_disp.loc[min_v][self.__axesY]], 
                                c='black', marker = "o",label="Minimum")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()],
                                [self.__data_disp.loc[max_v][self.__axesY],self.__data_disp.loc[max_v][self.__axesY]],
                                c='green', marker = "o", label="Maximum")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [mean, mean], 
                                c='red',label="Mean")
            self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [median,median],
                                c='cyan', marker = "P",label="Median")
        self.__axis.set_xlabel(self.__axesX)
        self.__axis.set_ylabel(self.__axesY)
        self.__box = self.__axis.get_position()
        self.__pos=self.__box.width * 0.7
        self.__axis.set_position([self.__box.x0, self.__box.y0, self.__pos, self.__box.height])
        self.__axis.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
        #self.__graph=self.simpleGraphe(self.__sliders)
        print('sliders',self.__sliders)#
        self.__graph=self.twoGraphes(self.__sliders)

    def sliders_on_changed(self,val):
        """Display a sliding bar controlling a variable.
        :param val: The variable to modify"""
        if self.sfreq!=None:
            self.__freq=self.sfreq.val
        if self.scores!=None:
            self.__core=self.scores.val
        if self.sinput!=None:
            self.__input=self.sinput.val
        if self.sfreq!=None and self.__axfreq.get_visible()==True:
            print('frequence',self.__freq)
            print('axfreq',self.__axfreq.get_visible())
            if self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==True and self.__axinput.get_visible()==True:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)
                                                &(self.__data["input"]==self.__input)]
            elif(self.scores!=None and self.sinput==None and self.__axcore.get_visible()==True)or(self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==True and self.__axinput.get_visible()==False):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)]
            elif(self.scores==None and self.sinput!=None and self.__axinput.get_visible()==True)or(self.scores!=None and self.sinput!=None and self.__axcore.get_visible()==False and self.__axinput.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["frequency"]==self.__freq)&(self.__data["input"]==self.__input)]
            else:
                self.__data_disp= self.__data[self.__data["frequency"]==self.__freq]
        if self.sinput!=None and self.__axinput.get_visible():
            print('axinput',self.__axinput.get_visible())
            if self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==True and self.__axfreq.get_visible()==True:
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["frequency"]==self.__freq)
                                                &(self.__data["input"]==self.__input)]
            elif(self.sfreq!=None and self.scores==None)or(self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==False and self.__axfreq.get_visible()==True):
                self.__data_disp= self.__data[(self.__data["input"]==self.__input)&(self.__data["frequency"]==self.__freq)]
            elif(self.sfreq==None and self.scores!=None)or(self.sfreq!=None and self.scores!=None and self.__axcore.get_visible()==True and self.__axfreq.get_visible()==False):
                self.__data_disp= self.__data[(self.__data["cores"]==self.__core)&(self.__data["input"]==self.__input)]
            else:
                self.__data_disp= self.__data[self.__data["input"]==self.__input]
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
        self.__fig1.subplots_adjust(bottom=0.2)
        self.__graphe=plt.subplots(111)
        self.__axcolor = 'lightgoldenrodyellow'
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
        """self.__graphe2=plt.subplots(132)
        self.__fig2.subplots_adjust(bottom=0.2)
        self.__axcolor = 'lightgoldenrodyellow'
        self.__names=['groupa','groupb','groupc']
        self.__values=['1','10','100']
        plot(names,values)
        self.__canvas=FigureCanvasTkAgg(self.__fig)
        self.__canvas.get_tk_widget().place(x=300,y=40)"""
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
        self.__axesX= val
        #self.updateType(self.__choice)

    def set_axeY(self, val):
        self.__axesY= val
        
    def updateType(self,choice):
    
        self.__axis.clear()
        self.__choice=choice
        temp=[]
        print('data_disp[self.__axesY]',self.__data_disp[self.__axesY])
        min_v= np.argmin(self.__data_disp[self.__axesY])
        max_v= np.argmax(self.__data_disp[self.__axesY])
        self.__axis=self.__fig1.add_subplot(111)
        for i in range (len(self.__data_disp[self.__axesX])):
            temp.append(self.__median[self.__axesY])
        mean= self.__data_disp[self.__axesY].mean()
        median= self.__data_disp[self.__axesY].median()
        self.__axis.set_title('Graphe')
        if not self.__data_disp.empty:
            if self.__choice == 'L':
                self.__axis.plot(self.__data_disp.loc[min_v][self.__axesX], self.__data_disp.loc[min_v][self.__axesY], 
                                    c='black', marker = "o",label="Minimum")
                self.__axis.plot(self.__data_disp.loc[max_v][self.__axesX], self.__data_disp.loc[max_v][self.__axesY], 
                                    c='green', marker = "o", label="Maximum")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [mean, mean], 
                                    c='red',label="Mean")
                self.__axis.plot(self.__data_disp[self.__axesX], temp,c='red', marker = "P",label="Median")
                self.__axis.plot(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x", ls='-')
            if self.__choice == 'B':    
                N=len(self.__data_disp[self.__axesX])
                #N=N+4
                ind = np.arange(N)
                width = 0.35
                self.__axis.bar(ind,self.__data_disp[self.__axesY],width,tick_label=self.__axesY)
                self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesX],width)
                self.__axis.bar(ind,self.__data_disp.loc[min_v][self.__axesY], width, color='black')
                self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesX], width)
                self.__axis.bar(ind,self.__data_disp.loc[max_v][self.__axesY], width, color='green')
                self.__axis.bar(ind,mean,width, color='red',tick_label="Mean")
                self.__axis.bar(ind,temp,width,color='red',tick_label="Median")
                self.__axis.bar(ind,self.__data_disp[self.__axesX],width,tick_label=self.__axesX)
            if self.__choice == 'P':
                self.__axis.scatter(self.__data_disp[self.__axesX],self.__data_disp[self.__axesY], marker = "x")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], 
                                    [self.__data_disp.loc[min_v][self.__axesY],self.__data_disp.loc[min_v][self.__axesY]], 
                                        c='black', marker = "o",label="Minimum")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], 
                                    [self.__data_disp.loc[max_v][self.__axesY],self.__data_disp.loc[max_v][self.__axesY]], 
                                        c='green', marker = "o", label="Maximum")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()],[mean, mean], 
                                        c='red',label="Mean")
                self.__axis.plot([self.__data_disp[self.__axesX].min(), self.__data_disp[self.__axesX].max()], [median,median],
                                        c='cyan', marker = "P",label="Median")
            self.__axis.set_xlabel(self.__axesX)
            self.__axis.set_ylabel(self.__axesY)
            self.__axis.set_position([self.__box.x0, self.__box.y0, self.__pos, self.__box.height])
            self.__axis.legend(loc='center left', bbox_to_anchor=(1, 0.5))
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
        self.__mask1=[0,0,0]
        self.__mask2=[0,0,0]
        self.__label_2=None
        self.__label_3=None
        self.__label_4=None
        self.__label_5=None
        self.__label_6=None
        self.__label_7=None
        self.__label_8=None
        self.__label_9=None
        self.__label_10=None
        self.__label_11=None
        self.__label_12=None
        self.__label_13=None
        self.__label_14=None
        self.__label_15=None
        self.__label_16=None
        self.__label_17=None
        self.__label_18=None
        self.__label_19=None
        self.__tkvar=StringVar()
        self.__tkvar1=StringVar()
        self.__tkvar2=StringVar()
        self.__tkvar3=StringVar()
        self.__tkvar4=StringVar()
        self.__choice='P'
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
        self.__master.title('Gecko')
        print(self.__setup.colorframe)
        self.__master.configure(bg=self.__setup.colorframe)
        self.MenuBar()
        choice=self.typeGraph()
        self.__graphe1=Graph1(data,self.__master,'P',self.__RHeight/2,self.__RWidth)
        print ('Graphe 2')
        self.__graphe2=Graph2(data,self.__master,'P',self.__RHeight/2,self.__RWidth)
        print('graphes')
        self.graphes(data.getData())
        self.__closebutton = Button(self.__master, text='X', command=self.quit)
        
    def graphes(self,data):
        """Creation of the graph.
        :param data: Data to draw"""
        var=[]
        self.__label_1=Label(self.__master,text='VARIABLES LIST',justify=LEFT).pack(expand=0,anchor='w')
        a=0
        for i in range (len(self.__confi["data_descriptor"])):
            vartemp=BooleanVar()
            var.append(vartemp)
            self.__mask1.append(0)
            self.__checkbutton_1=Checkbutton(self.__master,text=self.__confi["data_descriptor"]["keys"][i],
                    variable=lambda index=i:var[index],onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',justify='left',
                    command=lambda index=i:self.update_text1(var,index)).pack(expand=0,anchor='w')
        print('testa')
        #for i in range (len(self.__confi["data_descriptor"])):
         #   vartemp=BooleanVar()
          #  var.append(vartemp)
           # self.__mask2.append(0)
            #self.__checkbutton_1=Checkbutton(self.__master,text=self.__confi["data_descriptor"]["keys"][i],
             #       variable=lambda index=i:var[index],onvalue=1,offvalue=0,bg='#4f81bd',anchor='w',justify='left',
              #      command=lambda index=i:self.update_text2(var,index)).pack(expand=0,anchor='w')
        self.choiceAxesX()
        self.choiceAxesY()
        
    def update_text1(self,var,i):
        if i==0:
            if self.__label_2==None:
                self.__mask1[0]=1
                self.__label_2=Label(self.__master,text='Cores',justify=LEFT)
                self.__label_2.place(x=100,y=10)
                self.__label_3=Label(self.__master,text='Minimum : '+str(self.__min["cores"]),justify=LEFT)
                self.__label_3.place(x=100,y=30)
                self.__label_4=Label(self.__master,text='Maximum : '+str(self.__max["cores"]),justify=LEFT)
                self.__label_4.place(x=100,y=50)
            else:
                self.__mask1[0]=0
                self.__label_2.destroy()
                self.__label_3.place_forget()
                self.__label_4.place_forget()
                self.__label_2=None
        if i==1:
            if self.__label_5==None:
                self.__mask1[1]=1
                self.__label_5=Label(self.__master,text='Frequency',justify=LEFT)
                self.__label_5.place(x=100,y=70)
                self.__label_6=Label(self.__master,text='Minimum : '+str(self.__min["frequency"]),justify=LEFT)
                self.__label_6.place(x=100,y=90)
                self.__label_7=Label(self.__master,text='Maximum : '+str(self.__max["frequency"]),justify=LEFT)
                self.__label_7.place(x=100,y=110)
            else:
                self.__mask1[1]=0
                self.__label_5.destroy()
                self.__label_6.place_forget()
                self.__label_7.place_forget()
                self.__label_5=None
        if i==2:        
            if self.__label_8==None:
                self.__mask1[2]=1
                self.__label_8=Label(self.__master,text='Input',justify=LEFT)
                self.__label_8.place(x=100,y=130)
                self.__label_9=Label(self.__master,text='Minimum : '+str(self.__min["input"]),justify=LEFT)
                self.__label_9.place(x=100,y=150)
                self.__label_10=Label(self.__master,text='Maximum : '+str(self.__max["input"]),justify=LEFT)
                self.__label_10.place(x=100,y=170)
            else:
                self.__mask1[2]=0
                self.__label_8.destroy()
                self.__label_9.place_forget()
                self.__label_10.place_forget()
                self.__label_8=None
        self.__graphe1.twoGraphes(self.__mask1)
    
    def update_text2(self,var,i):
        if i==3:        
            if self.__label_11==None:
                self.__mask2[0]=1
                self.__label_11=Label(self.__master,text='Input',justify=LEFT)
                self.__label_11.place(x=100,y=190)
                self.__label_12=Label(self.__master,text='Minimum : '+str(self.__min["input"]),justify=LEFT)
                self.__label_12.place(x=100,y=210)
                self.__label_13=Label(self.__master,text='Maximum : '+str(self.__max["input"]),justify=LEFT)
                self.__label_13.place(x=100,y=230)
            else:
                self.__mask2[0]=0
                self.__label_11.destroy()
                self.__label_12.place_forget()
                self.__label_13.place_forget()
                self.__label_11=None
        if i==4:        
            if self.__label_12==None:
                self.__mask2[1]=1
                self.__label_12=Label(self.__master,text='Input',justify=LEFT)
                self.__label_12.place(x=100,y=130)
                self.__label_13=Label(self.__master,text='Minimum : '+str(self.__min["input"]),justify=LEFT)
                self.__label_13.place(x=100,y=150)
                self.__label_14=Label(self.__master,text='Maximum : '+str(self.__max["input"]),justify=LEFT)
                self.__label_14.place(x=100,y=170)
            else:
                self.__mask2[1]=0
                self.__label_12.destroy()
                self.__label_13.place_forget()
                self.__label_14.place_forget()
                self.__label_12=None
        if i==5:        
            if self.__label_17==None:
                self.__mask2[2]=1
                self.__label_17=Label(self.__master,text='Input',justify=LEFT)
                self.__label_17.place(x=100,y=250)
                self.__label_18=Label(self.__master,text='Minimum : '+str(self.__min["input"]),justify=LEFT)
                self.__label_18.place(x=100,y=270)
                self.__label_19=Label(self.__master,text='Maximum : '+str(self.__max["input"]),justify=LEFT)
                self.__label_19.place(x=100,y=290)
            else:
                self.__mask2[2]=0
                self.__label_17.destroy()
                self.__label_18.place_forget()
                self.__label_19.place_forget()
                self.__label_17=None
        if i==6:
            for a in range (len(self.__mask1)):
                self.__mask1[a]=0
                self.__mask2[a]=0
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
        
        #self.__graphe2.twoGraphes(self.__mask2)
                                    
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
        #self.__filemenu.add_command(label="Two graphs", command=self.two)
        #self.__filemenu.add_command(label="One graph", command=self.one)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Exit", command=self.quit)
    
    def reset(self):
        self.__graphe.reset()
        self.update_text2(None,6)
        self.uncheckall(3,self.__cbs)

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
        self.__graphe1.updateType(self.__choice)
        #self.__graphe2.updateType(self.__choice)
    
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
        self.__graphe1.set_axeX(self.__tkvar1.get())
        self.updateGraph()

    def change_dropdownAxesY(self,*args):
        self.__graphe1.set_axeY(self.__tkvar2.get())
        self.updateGraph()
    
    def change_dropdownAxesX1(self,*args):
        #self.__graphe2.set_axeX1(self.__tkvar4.get())
        self.updateGraph()

    def change_dropdownAxesY1(self,*args):
        #self.__graphe2.set_axeY1(self.__tkvar3.get())
        self.updateGraph()
    
    def save(self):
        name=self.__name.split("\\")
        temp=name[6].replace('completo_',' ')
        graph1=self.__graphe1.getGraph()
        #graph2=self.__graphe2.getGraph()
        listeval1=self.__graphe1.getVal()
        #listeval2=self.__graphe2.getVal()
        text=''' '''
        self.__saveGraph.saveJson(temp,self.datas,self.__tkvar1.get(),self.__tkvar4.get(),self.__tkvar2.get(),self.__tkvar3.get())
        for i in range(len(self.__confi["data_descriptor"])):
            print(self.__confi["data_descriptor"]["keys"][i])
            text = text+'''Filter on '''+self.__confi["data_descriptor"]["keys"][i]+''':'''+str(listeval1[i])
        #for i in range(len(self.__confi["data_descriptor"])):
        #    print(self.__confi["data_descriptor"]["keys"][i])
        #    text = text+'''Filter on '''+self.__confi["data_descriptor"]["keys"][i]+''':'''+str(listeval2[i])
        print(text)
        #graph.text(.1,.1,text)
        self.__saveGraph.savePDF(temp,graph1,self.__tkvar1.get(),self.__tkvar4.get(),self.__tkvar2.get(),self.__tkvar3.get(),text)
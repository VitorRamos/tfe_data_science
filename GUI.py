# -*- coding: utf-8 -*- 
import pandas as pd
import inspect,os,matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')
from pylab import plot,axis,savefig,show,title
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
#from matplotlib.lines import Line2D
class Graph:
    def __init__(self):
        #self.fig=Figure(figsize=(12,8))
        self.fig = Figure(figsize=(12,8), dpi=50)
        self.ax1 = self.fig.add_subplot(111)
    #def read(self):
        #wine_reviews=pd.read_csv("d:\Profiles\igauthier\Downloads/beatsdataset.csv")
        #plot([1,2,3,4],[1,4,9,16])
        #axis([1,4,0,16])
        #title('my curve')
        #savefig('acurvesaved.png')
        #show()
    def sliders_on_changed(self,val):
        freq=self.sfreq.val
        l,=plt.plot(np.arange(0.0, 1.0, 0.001),5*np.sin(2*np.pi*3*np.arange(0.0, 1.0, 0.001)),lw=2)
        l.set_ydata(2*np.pi*freq)
        self.fig.canvas.draw_idle()
    def simpleGraphe(self,master):
        canvas=FigureCanvasTkAgg(self.fig,master=master)
        #canvas.columnconfigure(1, pad=3)
        canvas.get_tk_widget().pack(side="right",padx=10)
        plt.subplots_adjust(bottom=0.25)
        plt.plot([1,2,3,4],[1,4,9,16])
        canvas.draw()
        axcolor = 'lightgoldenrodyellow'
        ax=self.fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
        self.sfreq=Slider(ax,'Freq',0.1, 30.0, valinit=3)
        self.sfreq.on_changed(self.sliders_on_changed)
    def twoGraphes(self):
        plt.subplots(131)
        ax=self.fig.add_axes([0.1,0.1,0.8,0.8])
        plt.subplots(132)
        names=['groupa','groupb','groupc']
        values=['1','10','100']
        plot(names,values)
        canvas=FigureCanvasTkAgg(self.fig)
        """canvas.show()"""
        canvas.get_tk_widget().place(x=300,y=40)
class MainWindow:
    def __init__(self,master,setup,graphe):
        self.setup=setup
        self.graphe=graphe
        """self.graphe.createWidgets()"""
        self.master=master
        """self.frame=Frame(self.master)"""
        self.initGUI()
    def initGUI(self):
        RWidth=self.master.winfo_screenwidth()
        RHeight=self.master.winfo_screenheight()
        self.master.geometry(str(RWidth)+"x"+str(RHeight))
        self.master.title('Test')
        self.master.configure(bg=self.setup._colorframe)
        self.graphes()
        """self.canvas1=tix.Canvas(self.master, width=390, height=600)
        self.canvas1.place(x=230,y=40)
        self.canvas1.config(bg=self.setup._colorframe,bd=0)"""
    def graphes(self):
        self.graphe.simpleGraphe(self.master)
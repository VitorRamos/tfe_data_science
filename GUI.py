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
from tkinter import filedialog, messagebox
from tkinter import *
#from matplotlib.lines import Line2D

class Graph:
    """ Class that read the draw the different graphes
        Attributes
            fig - The frame of the graph to draw
            ax1 - The choose of the datas to draw
        Methods
            sliders_on_changed()
            simpleGraphe()
            twoGraphes()"""

    def __init__(self,data):
        """ Create a empty object and initialize attributes."""
        #self.fig=Figure(figsize=(12,8))
        self.fig = Figure(figsize=(12,8), dpi=50)
        self.ax1 = self.fig.add_subplot(111).plot(data["frequency"],data["total_time"])
    #def read(self):
        #wine_reviews=pd.read_csv("d:\Profiles\igauthier\Downloads/beatsdataset.csv")
        #plot([1,2,3,4],[1,4,9,16])
        #axis([1,4,0,16])
        #title('my curve')
        #savefig('acurvesaved.png')
        #show()

    def sliders_on_changed(self,val):
        """Display a sliding bar controlling a variable.
        :param val: The variable to modify"""
        freq=self.sfreq.val
        l,=plt.plot(np.arange(0.0, 1.0, 0.001),5*np.sin(2*np.pi*3*np.arange(0.0, 1.0, 0.001)),lw=2)
        l.set_ydata(2*np.pi*freq)
        a=self.fig.canvas.draw_idle()

    def simpleGraphe(self,master,data):
        """The graph to draw.
        :param master: The window where to draw the graph.
        :param data: The data to draw."""
        canvas=FigureCanvasTkAgg(self.fig,master=master)
        #canvas.columnconfigure(1, pad=3)
        canvas.get_tk_widget().pack(side="right",padx=10)
        plt.subplots_adjust(bottom=0.25)
        #plt.add_subplot(111).plot(data["frequency"],data["cores"])
        canvas.draw()
        axcolor = 'lightgoldenrodyellow'
        ax=self.fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
        self.sfreq=Slider(ax,'Freq',0.1, 30.0, valinit=3)
        self.sfreq.on_changed(self.sliders_on_changed)

    def twoGraphes(self):
        """Creating to graph to compare them."""
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

    def __init__(self,master,setup,graphe,data,conf):
        """ Create a empty object and initialize attributes and GUI with graphe and initGUI methods.
        :param data: Data to draw"""
        self.setup=setup
        self.graphe=graphe
        """self.graphe.createWidgets()"""
        self.master=master
        """self.frame=Frame(self.master)"""
        self.confi=conf
        self.initGUI(data)
    
    def initGUI(self,data):
        """Creation of the different object.
        :param data: Data to display"""
        RWidth=self.master.winfo_screenwidth()
        RHeight=self.master.winfo_screenheight()
        self.master.geometry(str(RWidth)+"x"+str(RHeight))
        self.master.title('Test')
        self.master.configure(bg=self.setup._colorframe)
        self.graphes(data)
        self.MenuBar()
        """self.canvas1=tix.Canvas(self.master, width=390, height=600)
        self.canvas1.place(x=230,y=40)
        self.canvas1.config(bg=self.setup._colorframe,bd=0)"""
    
    def graphes(self,data):
        """Creation of the graph.
        :param data: Data to draw"""
        var=[]
        self.graphe.simpleGraphe(self.master,data)
        print(len(self.confi["data_descriptor"]))
        #for i in len(self.confi["data_descriptor"]):
         #   var[i]=IntVar()
          #  Checkbutton(self.master,text=data["data_descriptor"][i],variable=var[i],foreground='white',
           #             bg='#4f81bd',anchor='w',justify='left').place(x=40+i,y=55+i)
        var1=IntVar()
        Checkbutton(self.master,text='Frequence',variable=var1,foreground='white',
                    bg='#4f81bd',anchor='w',justify='left').place(x=40,y=55)
    
    def MenuBar(self):
        """This method is called by the initialisation of the interface to 
        create a bar with the different menu."""
        menu = Menu(self.master)
        self.master.config(menu=menu)
        #create the different menu.
        filemenu = Menu(menu)
        howtomenu=Menu(menu)
        var9=IntVar()
        var10=IntVar()
        var11=IntVar()
        var12=IntVar()
        var13=IntVar()
        menu.add_cascade(label="Menu", menu=filemenu)
        menu.add_cascade(label="Information", menu=howtomenu)
        #create the different option for the menus.
        howtomenu.add_command(label="Help")
        howtomenu.add_command(label='Loading files')
        howtomenu.add_command(label="aa")      
        filemenu.add_command(label="bb")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
    
    def quit(self):
        """This method is called by the pushing on the 'Exit' menu to close the
        software."""
        if messagebox.askyesno('Verify', 'Do you really to quit?'):
            sys.exit()
    
    def ok(self):
        """This method is called by the 'quit' method to close the main window."""
        self.master.withdraw()
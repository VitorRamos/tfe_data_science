# -*- coding: utf-8 -*- 
import pandas as pd
import inspect,os,matplotlib
import matplotlib.pyplot as plt
#import numpy as np
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

    def __init__(self,data,master, max, min):
        """ Create a empty object and initialize attributes."""
        self.__master=master
        self.__data=data
        self.__fig = Figure(figsize=(12,8), dpi=50)
        self.__canvas=FigureCanvasTkAgg(self.__fig,master=self.__master)
        self.__data_disp=data[(data["frequency"]==1200000)]
        self.__canvas.get_tk_widget().place(x=650,y=10)
        self.__max=max
        self.__min=min
        self.__ax1,  = self.__fig.add_subplot(111).plot(self.__data_disp["input"],
                                    self.__data_disp["total_time"])
        self.__graph=self.simpleGraphe(data)   

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
        self.__freq=self.sfreq.val
        #self.__ax1.set_xdata(2*self.__freq)
        self.__data_disp=self.__data[(self.__data["frequency"]==self.__freq)]
        self.__ax1.set_ydata(2*self.__data_disp["total_time"])
        self.__a=self.__fig.canvas.draw_idle()

    def simpleGraphe(self,data):
        """The graph to draw.
        :param master: The window where to draw the graph.
        :param data: The data to draw."""
        #canvas.columnconfigure(1, pad=3)
        #self.__graphe=plt.subplots_adjust(bottom=0.25)
        #plt.add_subplot(111).plot(data["frequency"],data["cores"])
        #self.__canvas.draw()
        self.__axcolor = 'lightgoldenrodyellow'
        self.__ax=self.__fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor=self.__axcolor)
        self.sfreq=Slider(self.__ax,'Freq',self.__min["frequency"],self.__max["frequency"], 
                                valinit=self.__min["frequency"],valstep=100000)
        self.sfreq.on_changed(self.sliders_on_changed)
        print(self.sfreq.val)
        self.__data_disp=data[(data["frequency"]==self.sfreq)]
        print(self.__data_disp["total_time"])
        #self.__canvas.show()
        #self.__fig.pause(0.01)

    @property
    def twoGraphes(self):
        """Creating to graph to compare them."""
        self.__graphe1=plt.subplots(131)
        self.__ax=self.__fig.add_axes([0.1,0.1,0.8,0.8])
        self.__graphe2=plt.subplots(132)
        self.__names=['groupa','groupb','groupc']
        self.__values=['1','10','100']
        plot(names,values)
        self.__canvas=FigureCanvasTkAgg(self.__fig)
        """canvas.show()"""
        self.__canvas.get_tk_widget().place(x=300,y=40)

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

    def __init__(self,master,setup,data,conf, max, min, median):
        """ Create a empty object and initialize attributes and GUI with graphe and initGUI methods.
        :param data: Data to draw"""
        self.__setup=setup
        """self.__graphe=Graph(datas)
        self.graphe.createWidgets()"""
        self.__master=master
        """self.frame=Frame(self.master)"""
        self.__confi=conf
        self.__max=max
        self.__min=min
        self.__median=median
        self.initGUI(data)

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
        self.graphes(data)
        self.__closebutton = Button(self.__master, text='X', command=self.quit)
        """self.canvas1=tix.Canvas(self.master, width=390, height=600)
        self.canvas1.place(x=230,y=40)
        self.canvas1.config(bg=self.setup._colorframe,bd=0)"""

    def graphes(self,data):
        """Creation of the graph.
        :param data: Data to draw"""
        var=[]
        """self.__graph=self.__graphe.simpleGraphe(self.__master,data)"""
        self.__label_1=Label(self.__master,text='VARIABLES LIST',justify=LEFT).pack(expand=0,anchor='w')
        for i in range (len(self.__confi["data_descriptor"])):
            var.append(IntVar(value=1))
            self.__checkbutton_1=Checkbutton(self.__master,text=self.__confi["data_descriptor"]["keys"][i],
                        variable=lambda index=i:var[index],foreground='white',onvalue=True,offvalue=False,
                        bg='#4f81bd',anchor='w',justify='left').pack(expand=0,anchor='w')
        self.__checkbutton_2=Checkbutton(self.__master,text=self.__confi["data_descriptor"]["values"],
                    variable=lambda index=i:var[index],foreground='white',onvalue=True,offvalue=False,
                    bg='#4f81bd',justify=LEFT).pack(expand=0,anchor='w')
        self.__label_2=Label(self.__master,text='Cores',justify=LEFT).place(x=650,y=410)
        self.__label_3=Label(self.__master,text='Minimum : '+str(self.__min["cores"]),justify=LEFT).place(x=650,
                                    y=430)
        self.__label_4=Label(self.__master,text='Maximum : '+str(self.__max["cores"]),justify=LEFT).place(x=650,
                                    y=450)
        self.__label_5=Label(self.__master,text='Frequency',justify=LEFT).place(x=650,y=470)
        self.__label_6=Label(self.__master,text='Minimum : '+str(self.__min["frequency"]),
                                    justify=LEFT).place(x=650,y=490)
        self.__label_7=Label(self.__master,text='Maximum : '+str(self.__max["frequency"]),
                                    justify=LEFT).place(x=650,y=510)
        self.__label_8=Label(self.__master,text='Input',justify=LEFT).place(x=650,y=530)
        self.__label_9=Label(self.__master,text='Minimum : '+str(self.__min["input"]),justify=LEFT).place(x=650,
                                    y=550)
        self.__label_10=Label(self.__master,text='Maximum : '+str(self.__max["input"]),justify=LEFT).place(x=650,
                                    y=570)
        #self.__label_11=Label(self.__master,text='Repetitions',justify=LEFT).pack(expand=0,anchor='w')
        #self.__label_12=Label(self.__master,text='Minimum : '+str(self.__min["repetitions"]),
         #                           justify=LEFT).pack(expand=0,anchor='w')
        #self.__label_13=Label(self.__master,text='Maximum : '+str(self.__max["repetitions"]),
          #                          justify=LEFT).pack(expand=0,anchor='w')
                                    
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
        self.__filemenu.add_command(label="Reset")
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Exit", command=self.quit)
    
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
        self.__label_2=Label(self.__master,text="Help: text to write").place(x=215,y=15,width=300,height=25)

    def load_file(self):
        """This method is called by the pushing on the 'Loading file' menu to 
        upload the right result file for the session."""
        #read the session file thanks to the object session.
        self.__name= filedialog.askopenfilename()
        print(self.__name)

    #def ask_quit(self):
     #   self.quit()
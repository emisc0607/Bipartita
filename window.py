#Window imports
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt

#Stats imports
import pyreadstat
import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

#Module imports
import proyeccion_CSV
#import proyeccion_SPSS

def onClickListener():
    m = method.get()
    if(m == 1):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        
    elif(m == 2):
        file_path = filedialog.askopenfilename(filetypes=[("EXCEL files", '*.xlsx')])

    elif(m == 3):
        file_path = filedialog.askopenfilename(filetypes=[("SPSS files", "*.sav")])
        
    else:
        messagebox.showinfo('Alert', 'Select a valid method')
    return

vn = tk.Tk()
vn.title("Proyección Bipartita con Louvain Final")
vn.geometry("250x300")
val = tk.Entry(vn, width = 10)
Label(vn, text= "x =").place(x= 70, y= 40)
val.place(x = 95, y = 40)
val2 = tk.Entry(vn, width = 10)
Label(vn, text= "v =").place(x= 70, y= 100)
val2.place(x = 95, y = 100)
Button(vn, text='Calcular', command=onClickListener).place(x=90, y=150)

method = tk.IntVar()
Radiobutton(vn, text='CSV', variable=method, value=1).place(x=95, y=200)
Radiobutton(vn, text='EXCEL', variable=method, value=2).place(x=95, y=225)
Radiobutton(vn, text='SPSS', variable=method, value=3).place(x=95, y=250)
vn.mainloop()
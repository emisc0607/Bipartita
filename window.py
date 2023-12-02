#Window imports
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
import sys


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
    if m == 1:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        text_widget = Text(vn, height=20, width=50)
        text_widget.pack()
        sys.stdout = text_widget
        proyeccion_CSV.bipartita_CSV(file_path, text_widget)
        sys.stdout = sys.__stdout__
    elif m == 2:
        file_path = filedialog.askopenfilename(filetypes=[("EXCEL files", '*.xlsx')])
        # Agregar lógica para manejar archivos Excel
    elif m == 3:
        file_path = filedialog.askopenfilename(filetypes=[("SPSS files", "*.sav")])
        # Agregar lógica para manejar archivos SPSS
    else:
        messagebox.showinfo('Alert', 'Select a valid method')
    return


#Ventana 
vn = tk.Tk()
vn.title("Proyección Bipartita con Louvain Final")
vn.geometry("450x500")

method = tk.IntVar()
Radiobutton(vn, text='CSV', variable=method, value=1).pack(pady=10)
Radiobutton(vn, text='EXCEL', variable=method, value=2).pack(pady=10)
Radiobutton(vn, text='SPSS', variable=method, value=3).pack(pady=10)
Button(vn, text='Calcular', command=onClickListener).pack(pady=10)
vn.mainloop()
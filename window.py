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

#Ventana 
vn = tk.Tk()
vn.title("Proyección Bipartita con Louvain Final")
vn.geometry("200x200")

#Manejo de archivos CSV
def CSV_manager(file_path, text_widget):

    base = pd.read_csv(file_path)
    text_widget.insert(tk.END, "Contenido del archivo CSV:\n")
    text_widget.insert(tk.END, str(base) + "\n")

    baseT = pd.melt(base, id_vars=["Persona"])
    baseT["Psicol"] = baseT['variable'].astype(str) + "_R_" + baseT['value'].astype(str)
    text_widget.insert(tk.END, "Transformación melt:\n")
    text_widget.insert(tk.END, str(baseT) + "\n")

    B = nx.Graph()
    B.add_nodes_from(baseT["Persona"].unique(), bipartite=0)
    B.add_nodes_from(baseT["Psicol"].unique(), bipartite=1)
    edges = baseT[["Persona", "Psicol"]].values.tolist()
    B.add_edges_from(edges)
    text_widget.insert(tk.END, "¿La gráfica es bipartita?: {}\n".format(bipartite.is_bipartite(B)))
    text_widget.insert(tk.END, "¿La gráfica es conexa?: {}\n".format(nx.is_connected(B)))

    Persona, Psicol = bipartite.sets(B)
    P = bipartite.weighted_projected_graph(B, Psicol)
    CPsi = nx.community.louvain_communities(P, weight='weight')
    df = pd.DataFrame(CPsi)
    dfT = df.transpose()
    dfT.to_csv('Comunidades_Psicol.csv', header=False, index=False)
    text_widget.insert(tk.END, "Comunidades Psicol CSV:\n")
    text_widget.insert(tk.END, str(dfT) + "\n")

    nx.write_gexf(P, "Proyeccion_Psicol.gexf")

    Q = bipartite.weighted_projected_graph(B, Persona)
    CPer = nx.community.louvain_communities(Q, weight='weight')
    df = pd.DataFrame(CPer)
    dfT = df.transpose()
    dfT.to_csv('Comunidades_Personas.csv', header=False, index=False)
    text_widget.insert(tk.END, "Comunidades Personas CSV:\n")
    text_widget.insert(tk.END, str(dfT) + "\n")

    nx.write_gexf(Q, "Proyeccion_Personas.gexf")

    text_widget.insert(tk.END, 'Done!\n')

#Manejo de archivos XLSX

#Manejo de archivos SAV

#Seleccion del tipo de archivo
def onClickListener():
    m = method.get()
    if m == 1:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        vn.geometry("450x500")
        text_widget = Text(vn)
        text_widget.pack(expand=True, fill='both')
        CSV_manager(file_path, text_widget)
    elif m == 2:
        file_path = filedialog.askopenfilename(filetypes=[("EXCEL files", '*.xlsx')])
        vn.geometry("450x500")
    elif m == 3:
        file_path = filedialog.askopenfilename(filetypes=[("SPSS files", "*.sav")])
    else:
        messagebox.showinfo('Alert', 'Select a valid method')

#Estructura de la ventana
method = tk.IntVar()
Radiobutton(vn, text='CSV', variable=method, value=1).pack(pady=10)
Radiobutton(vn, text='EXCEL', variable=method, value=2).pack(pady=10)
Radiobutton(vn, text='SPSS', variable=method, value=3).pack(pady=10)
Button(vn, text='Calcular', command=onClickListener).pack(pady=10)
vn.mainloop()
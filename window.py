# Window imports
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
import sys

# Stats imports
import pyreadstat
import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

# Ventana
vn = tk.Tk()
vn.title("Proyección Bipartita con Louvain Final")
vn.geometry("200x200")


# Manejo de archivos CSV
def csv_manager(file_path, text_widget):
    base = pd.read_csv(file_path)
    base_t = pd.melt(base, id_vars=["Persona"])
    base_t["Psicol"] = base_t['variable'].astype(str) + "_R_" + base_t['value'].astype(str)

    b = nx.Graph()
    b.add_nodes_from(base_t["Persona"].unique(), bipartite=0)
    b.add_nodes_from(base_t["Psicol"].unique(), bipartite=1)
    edges = base_t[["Persona", "Psicol"]].values.tolist()
    b.add_edges_from(edges)
    if bipartite.is_bipartite(b):
        messagebox.showinfo(title="Informacion", message="La gráfica es bipartita")
        if nx.is_connected(b):
            messagebox.showinfo(title="Informacion", message="La gráfica es conexa")
            # Modificacion de la ventana
            vn.geometry("400x300")
            # Generacion de la proyeccion
            text_widget.insert(tk.END, "Contenido del archivo CSV:\n")
            text_widget.insert(tk.END, str(base) + "\n")
            persona, psicol = bipartite.sets(b)
            p = bipartite.weighted_projected_graph(b, psicol)
            c_psi = nx.community.louvain_communities(p, weight='weight')
            df = pd.DataFrame(c_psi)
            df_t = df.transpose()
            df_t.to_csv('Comunidades_Psicol.csv', header=False, index=False)
            nx.write_gexf(p, "Proyeccion_Psicol.gexf")
            q = bipartite.weighted_projected_graph(b, persona)
            c_per = nx.community.louvain_communities(q, weight='weight')
            df = pd.DataFrame(c_per)
            df_t = df.transpose()
            df_t.to_csv('Comunidades_Personas.csv', header=False, index=False)
            nx.write_gexf(q, "Proyeccion_Personas.gexf")
            messagebox.showinfo(title="¡Listo!", message="Proyección generada")
        else:
            messagebox.showerror(title="Error", message="La gráfica no es conexa")
    else:
        messagebox.showerror(title="Error", message="La gráfica no es bipartita")


# Manejo de archivos XLSX

# Manejo de archivos SAV

# Seleccion del tipo de archivo
def onclick():
    m = method.get()
    if m == 1:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        text_widget = Text(vn)
        text_widget.pack(expand=True, fill='both')
        csv_manager(file_path, text_widget)
    elif m == 2:
        file_path = filedialog.askopenfilename(filetypes=[("EXCEL files", '*.xlsx')])
        vn.geometry("450x500")
    elif m == 3:
        file_path = filedialog.askopenfilename(filetypes=[("SPSS files", "*.sav")])
    else:
        messagebox.showinfo('Alert', 'Select a valid method')


# Estructura de la ventana
method = tk.IntVar()
Radiobutton(vn, text='CSV', variable=method, value=1).pack(pady=10)
Radiobutton(vn, text='EXCEL', variable=method, value=2).pack(pady=10)
Radiobutton(vn, text='SPSS', variable=method, value=3).pack(pady=10)
Button(vn, text='Calcular', command=onclick).pack(pady=10)
vn.mainloop()

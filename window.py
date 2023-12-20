# Window imports
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

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
        # Modificacion de la ventana
        vn.geometry("400x450")
        # Generacion de la proyeccion
        text_widget.insert(tk.END, "Contenido del archivo CSV:\n")
        text_widget.insert(tk.END, str(base) + "\n")
        if nx.is_connected(b):
            messagebox.showinfo(title="Informacion", message="La gráfica es conexa")
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
def xlsx_manager(file_path, text_widget):
    base = pd.read_excel(file_path)
    base_t = pd.melt(base, id_vars=["Persona"])
    base_t["Psicol"] = base_t['variable'].astype(str) + "_R_" + base_t['value'].astype(str)
    b = nx.Graph()
    b.add_nodes_from(base_t["Persona"].unique(), bipartite=0)
    b.add_nodes_from(base_t["Psicol"].unique(), bipartite=1)
    edges = base_t[["Persona", "Psicol"]].values.tolist()
    b.add_edges_from(edges)
    if bipartite.is_bipartite(b):
        messagebox.showinfo(title="Informacion", message="La gráfica es bipartita")
        # Modificacion de la ventana
        vn.geometry("400x450")
        text_widget.insert(tk.END, "Contenido del archivo XLSX:\n")
        text_widget.insert(tk.END, str(base) + "\n")
        if nx.is_connected(b):
            messagebox.showinfo(title="Informacion", message="La gráfica es conexa")
            # Generacion de la proyeccion
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


# Manejo de archivos SAV
def sav_manager(file_path, text_widget):
    data, metadata = pyreadstat.read_sav(file_path)
    data_reshaped = data.melt(id_vars=["Persona"], var_name="Reactivo", value_name="Respuesta")
    data_reshaped["Psicol"] = data_reshaped["Reactivo"] + "_R_" + data_reshaped["Respuesta"].astype(str)
    b = nx.Graph()
    b.add_nodes_from(data_reshaped["Persona"].unique(), bipartite=0)
    b.add_nodes_from(data_reshaped["Psicol"].unique(), bipartite=1)
    edges = data_reshaped[["Persona", "Psicol"]].values.tolist()
    b.add_edges_from(edges)
    if bipartite.is_bipartite(b):
        messagebox.showinfo(title="Informacion", message="La gráfica es bipartita")
        # Modificacion de la ventana
        vn.geometry("400x450")
        text_widget.insert(tk.END, "Contenido del archivo XLSX:\n")
        text_widget.insert(tk.END, str(data_reshaped) + "\n")
        nx.write_gexf(b, "Bipartita_original.gexf")
        if nx.is_connected(b):
            messagebox.showinfo(title="Informacion", message="La gráfica es conexa")
            # Comportamiento Conexo
            persona, psicol = bipartite.sets(b)
            p = bipartite.weighted_projected_graph(b, psicol)
            c_psi = nx.community.louvain_communities(p, weight='weight')
            df = pd.DataFrame(c_psi)
            df_t = df.transpose()
            df_t.to_csv('Comunidades_Psicol.csv', header=False, index=False)
            nx.write_gexf(p, "Proyeccion_Psicol.gexf")
            Q = bipartite.weighted_projected_graph(b, persona)
            c_per = nx.community.louvain_communities(Q, weight='weight')
            df = pd.DataFrame(c_per)
            df_t = df.transpose()
            df_t.to_csv('Comunidades_Personas.csv', header=False, index=False)
            nx.write_gexf(Q, "Proyeccion_Personas.gexf")
            messagebox.showinfo(title="¡Listo!", message="Proyección generada")
        else:
            messagebox.showerror(title="Error", message="La gráfica no es conexa")
    else:
        messagebox.showerror(title="Error", message="La gráfica no es bipartita")


# Seleccion del tipo de archivo
def onclick():
    m = method.get()
    text_widget = Text(vn)
    if m == 1:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        text_widget.pack(expand=True, fill='both')
        csv_manager(file_path, text_widget)
    elif m == 2:
        file_path = filedialog.askopenfilename(filetypes=[("EXCEL files", '*.xlsx')])
        text_widget.pack(expand=True, fill='both')
        xlsx_manager(file_path, text_widget)
    elif m == 3:
        file_path = filedialog.askopenfilename(filetypes=[("SPSS files", "*.sav")])
        text_widget.pack(expand=True, fill='both')
        sav_manager(file_path, text_widget)
    else:
        messagebox.showinfo('Alert', 'Select a valid method')


# Estructura de la ventana
method = tk.IntVar()
Radiobutton(vn, text='CSV', variable=method, value=1).pack(pady=10)
Radiobutton(vn, text='EXCEL', variable=method, value=2).pack(pady=10)
Radiobutton(vn, text='SPSS', variable=method, value=3).pack(pady=10)
Button(vn, text='Calcular', command=onclick).pack(pady=10)
vn.mainloop()

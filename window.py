import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import pyreadstat
import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

# Ventana
vn = tk.Tk()
vn.title("Proyección Bipartita con Louvain Final")
vn.geometry("380x420")


# Función para limpiar el contenido del widget de texto
def clear_text_widget(text_widget1):
    text_widget1.delete(1.0, tk.END)


# Función para manejar archivos CSV
def csv_manager(file_path, text_widget1):
    clear_text_widget(text_widget1)
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
        text_widget1.insert(tk.END, "Contenido del archivo CSV:\n")
        text_widget1.insert(tk.END, str(base) + "\n")
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


# Función para manejar archivos XLSX
def xlsx_manager(file_path, text_widget1):
    clear_text_widget(text_widget1)
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
        text_widget1.insert(tk.END, "Contenido del archivo XLSX:\n")
        text_widget1.insert(tk.END, str(base) + "\n")
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


# Función para manejar archivos SAV
def sav_manager(file_path, text_widget1):
    clear_text_widget(text_widget1)
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
        text_widget1.insert(tk.END, "Contenido del archivo XLSX:\n")
        text_widget1.insert(tk.END, str(data_reshaped) + "\n")
        nx.write_gexf(b, "Bipartita_original.gexf")
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


# Seleccion del tipo de archivo
def onclick():
    m = method.get()
    if m == 1:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        csv_manager(file_path, text_widget)
    elif m == 2:
        file_path = filedialog.askopenfilename(filetypes=[("EXCEL files", '*.xlsx')])
        text_widget.pack(expand=True, fill='both', padx=10)
        xlsx_manager(file_path, text_widget)
    elif m == 3:
        file_path = filedialog.askopenfilename(filetypes=[("SPSS files", "*.sav")])
        text_widget.pack(expand=True, fill='both')
        sav_manager(file_path, text_widget)
    else:
        messagebox.showinfo('Alert', 'Select a valid method')


# Estructura de la ventana
method = tk.IntVar()
Label(vn, text='Contenido del archivo', justify="left", font=('arial bold', 12)).pack(pady=10)
text_widget = Text(vn, height=15)
text_widget.pack(expand=True, fill='x')
frame1 = Label(vn)
frame1.pack()
frame2 = LabelFrame(frame1, text='Seleccione el tipo de archivo', padx=30, pady=10)
Radiobutton(frame2, text='CSV', font=12, variable=method, value=1, justify='left').grid(row=0, column=1, padx=5)
Radiobutton(frame2, text='EXCEL', font=12, variable=method, value=2, justify='left').grid(row=0, column=2, padx=5)
Radiobutton(frame2, text='SPSS', font=12, variable=method, value=3, justify='left').grid(row=0, column=3, padx=5)
frame2.grid(row=3, columnspan=3, padx=30)
Button(vn, text='Seleccionar archivo', font=('arial bold', 12), command=onclick).pack(side="bottom", pady=10)
vn.mainloop()

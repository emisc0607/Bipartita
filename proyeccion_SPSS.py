import pyreadstat
import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

#Abrir el archivo .sav del programa SPSS
data, metadata = pyreadstat.read_sav("EjBase.sav")

# Crea la base de datos para usarla para crear la gráfica bipartita
# Trasponer los reactivos y concatenarlos, crea una nueva columna con el reactivo y la respuesta psicológica
# Asignar la ID a la variable Persona y asignar Reactivo+_R_+Respuestas psicológicas
data_reshaped = data.melt(id_vars=["Persona"] , var_name="Reactivo", value_name="Respuesta")
data_reshaped["Psicol"] = data_reshaped["Reactivo"] + "_R_" + data_reshaped["Respuesta"].astype(str)
print(data_reshaped)

#Crea una gráfica 
B = nx.Graph()

#Añade a las Personas a un subconjunto de nodos y los Items al otro subconjunto
B.add_nodes_from(data_reshaped["Persona"].unique(), bipartite=0)
B.add_nodes_from(data_reshaped["Psicol"].unique(), bipartite=1)

# Añade aristas que conectan a las personas con sus respuestas psicológicas
edges = data_reshaped[["Persona", "Psicol"]].values.tolist()
B.add_edges_from(edges)

# Esta parte es solo para verificar que tenemos una gráfica bipartita
# la pueden omitir posteriormente
print("la gráfica es bipartita =")
print(bipartite.is_bipartite(B))

#Guardar la gráfica bipartita original para abrirla en Gephi
nx.write_gexf(B,"Bipartita_original.gexf")

# Evaluar si la gráfica es conexa, servirá para el método de proyección ponderada
# esta parte es importante pues si no es conexa al realizar el procedimiento
# de proyección nos dara un mensaje de error y se detendrá el programa
print("la gráfica es conexa =", nx.is_connected(B))

#Si es conexa se realizará el siguiente procedimiento de proyección ponderada
Persona, Psicol = bipartite.sets(B)

#Proyección ponderada del conjunto de respuestas psicológicas
P = bipartite.weighted_projected_graph(B, Psicol)

#Comunidades en las respuestas psicológicas. Aplica el algoritmo de Louvain para identificar las comunidades
#las cuáles se guardarán en el archivo Comunidades_Psicol.gexf 
CPsi=nx.community.louvain_communities(P,weight='weight')
df=pd.DataFrame(CPsi)
dfT=df.transpose()
dfT.to_csv('Comunidades_Psicol.csv', header = False, index = False)

# Guardar la gráfica proyectada de las respuestas psicológicas como archivo para usarlo con Gephi
nx.write_gexf(P,"Proyeccion_Psicol.gexf")

#Proyeccion ponderada del conjunto de Personas
Q = bipartite.weighted_projected_graph(B, Persona)

#Comunidades en Personas. Aplica el algoritmo de Louvain para identificar comunidades en las personas
CPer=nx.community.louvain_communities(Q,weight='weight')
df=pd.DataFrame(CPer)
dfT=df.transpose()
dfT.to_csv('Comunidades_Personas.csv', header = False, index = False)

#Guardar la gráfica proyectada de las Personas como archivo para usarlo con Gephi
nx.write_gexf(Q,"Proyeccion_Personas.gexf")
print('Done')

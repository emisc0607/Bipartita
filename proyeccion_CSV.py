import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

def main():
    # Si el archivo tiene extensión .csv usar este comando
    #recuerden agregar un # antes de base = pd.read_excel()para que no se ejecute
    base = pd.read_csv("BaseEjem.csv")

    # Si el archivo es tipo excel usar este comando, en algunos casos con pandas
    # se genera un mensaje de error y se solocitará instalar openpyxl para que lea
    # los archivos excel, esto se puede hacer con el siguiente comando: pip install openpyxl
    # recuerden agregar un # en base = pd.read_csv() para que no se ejecute 

    base = pd.read_excel("Base_Habitab.xlsx")

    #Para verificar los datos que se importaron se pueden ver con la siguiente instrucción
    print(base)

    #Se crea la base de datos para crear la gráfica bipartita
    baseT= pd.melt(base, id_vars=["Persona"])
    baseT["Psicol"]=baseT['variable'].astype(str)+"_R_"+baseT['value'].astype(str)
    # Para verificar la base de datos que se creo
    print(baseT)

    #Crea una gráfica bipartita
    B = nx.Graph()

    #Añade a las Personas a un subconjunto de nodos y los Items al otro subconjunto
    B.add_nodes_from(baseT["Persona"].unique(), bipartite=0)
    B.add_nodes_from(baseT["Psicol"].unique(), bipartite=1)

    # Añade aristas que conectan a las personas con sus respuestas psicológicas
    edges = baseT[["Persona", "Psicol"]].values.tolist()
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

    print('Done!')

def bipatita_CSV(file_path):
    base = pd.read_csv(file_path)
    print(base)
    baseT= pd.melt(base, id_vars=["Persona"])
    baseT["Psicol"]=baseT['variable'].astype(str)+"_R_"+baseT['value'].astype(str)
    print(baseT)

    #Crea una gráfica bipartita
    B = nx.Graph()

    #Añade a las Personas a un subconjunto de nodos y los Items al otro subconjunto
    B.add_nodes_from(baseT["Persona"].unique(), bipartite=0)
    B.add_nodes_from(baseT["Psicol"].unique(), bipartite=1)

    # Añade aristas que conectan a las personas con sus respuestas psicológicas
    edges = baseT[["Persona", "Psicol"]].values.tolist()
    B.add_edges_from(edges)

    # Esta parte es solo para verificar que tenemos una gráfica bipartita
    # la pueden omitir posteriormente
    print("la gráfica es bipartita =")
    print(bipartite.is_bipartite(B))
    print("la gráfica es conexa =", nx.is_connected(B))
    return
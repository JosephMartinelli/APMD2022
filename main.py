#Progetto creato da: Giuseppe Martinelli & Sindi Ruci
#
#
#


import random
import re
import networkx as nx
from Utility import *

# Variabili Globali
id = 0
actor_dic = {}
movie_dic = {}
reverse_movie = {}
reverse_actor = {}
movie_actors_dic = {}
edge_list = []
G = nx.MultiGraph()





############################################################################
# ******************** Modo efficiente per analizzare sequenzialmente il file in pandas? *************
# https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
# https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#essential-basic-functionality
# Per iterare tutto il dataframe e non morire nella complessità come possiamo fare? (dal primo link)
# 1.Vectorization
# 2.Cython routines
# 3.List Comprehensions (vanilla for loop)
# 4.DataFrame.apply(): i)  Reductions that can be performed in Cython, ii) Iteration in Python space
# 5.DataFrame.itertuples() and iteritems()
# 6.DataFrame.iterrows()

def create_graph(data):
    global G
    start_time()
    print("################# Costruzione dizionari ###########################")
    for x, y in zip(data[0], data[1]):
        build_dictionaries_and_graph(x, y)
    stop_time()
    print("Numero attori: ",len(actor_dic.keys()))
    print("Numero film: ",len(movie_dic.keys()))
    print("###################################################################")
    print("############# Creazione grafo ##############")
    start_time()
    G.add_nodes_from(list(movie_dic.values()))
    G.add_edges_from(edge_list)
    stop_time()
    print("Dump dei dati dalla memoria")
    del data


def build_dictionaries_and_graph(x, y):
    global actor_dic
    global movie_dic
    global reverse_movie
    global id
    global movie_actors_dic
    global reverse_actor
    global movie_year_index

    actor_id = actor_dic.get(x)
    movie_id = movie_dic.get(y)

    #Estrazione anno
    try:
        #Spiegazione regex:
        # cerca una stringa che comincia con '(' al suo interno contiene 4 caratteri ognuno con valore tra [0-9],
        # la stringa deve terminare con ')'
        year = re.search(r"\(([0-9]{4})\)", y).group(1)

    except:
        # se il film non presenta l'anno, allora si utilizza un valore fittizzio pari a '9999'
        year = "9999"

    if actor_id is None and movie_id is None:
        actor_dic.update({x: id})
        movie_dic.update({y: (id+1, {"anno": year})})
        reverse_actor.update({id: x})
        reverse_movie.update({id+1: y})
        edge_list.append((id, id + 1))
        movie_actors_dic.update({id+1: [id]})
    elif actor_id is None:
        movie_id = movie_id[0]
        actor_dic.update({x: id})
        reverse_actor.update({id:x})
        edge_list.append((id, movie_id))
        list_actor = movie_actors_dic.get(movie_id)
        list_actor.append(id)
        movie_actors_dic.update({movie_id:list_actor})
    elif movie_id is None:
        movie_dic.update({y: (id+1, {"anno": year})})
        reverse_movie.update({id+1: y})
        edge_list.append((actor_id, id + 1))
        movie_actors_dic.update({id+1:[actor_id]})
    else:
        movie_id = movie_id[0]
        edge_list.append((actor_id, movie_id))
        list_actor = movie_actors_dic.get(movie_id)
        list_actor.append(actor_id)
        movie_actors_dic.update({movie_id: list_actor})
    id += 2


def find_film_with_max_actors(x):
    start_time()
    max = 0
    film_id = 0
    for val in movie_dic.values():
        degree = G.degree[val[0]]
        if int(val[1]["anno"]) <= x and degree > max:
            max = degree
            film_id = val[0]
    stop_time()
    return reverse_movie.get(film_id), max


def resolve_question_1():
    while True:
        print("Inserire un anno per sapere quale è il film con il maggiore numero di attori")
        x = int(input())
        film, attori = find_film_with_max_actors(x)
        print(film + "\tNumero attori: ", attori)
        print("Altro titolo? [y/n]")
        choiche = str(input()).lower()
        if choiche == "n":
            return
        elif choiche != "y" or choiche != "n":
            print("Valore inserito non corretto, scegli uno tra [y/n]")


def connected_component(year):
    start_time()
    global G
    G1 = nx.MultiGraph()
    for val in movie_dic.values():
        if int(val[1]["anno"]) <= year:
            for x in list(G.neighbors(val[0])):
                G1.add_edge(val[0], x)
    stop_time()
    start_time()
    print("Costruzione della componente connessa più grande")
    return G.subgraph(max(nx.connected_components(G1), key=len))


def calculate_fringe(graph,source_node):
    return nx.shortest_path_length(graph, source=source_node)


def calculate_b_i(graph, targets, distance):
    fringe_of_source = calculate_fringe_at_distance(targets, distance)
    nodes = list(fringe_of_source.keys())
    ecc = nx.eccentricity(graph, v=nodes)
    return max(ecc.values())


def calculate_fringe_at_distance(targets, distance):
    return dict(filter(lambda elem: elem[1] == distance, targets.items()))


def middle_node_of_2_sweep(graph):
    print("Esecuzione di 2-Sweep")
    start_time()
    #Selezioniamo un nodo a caso
    node = random.choice(list(graph.nodes()))
    print("Nodo scelto casualmente: ",node)
    #In altre parole prendiamo il nodo a distanza massima dal nodo scelto precedentemente
    a_paths = nx.single_source_shortest_path_length(graph,node)
    #Ci ricalcoliamo le shortest_path di lunghezza massima dal valore trovato precedentemente
    b_paths = nx.single_source_shortest_path(graph,list(a_paths.keys())[len(a_paths.keys())-1])
    diametral_path = list(b_paths.values())[len(b_paths.values()) - 1]
    print("Nodo trovato: ", diametral_path[int(len(diametral_path) / 2)])
    stop_time()
    return diametral_path[int(len(diametral_path) / 2)]


def resolve_question_2(year=None,saveOnFile=False):
    if year is None:
        print("Inserisci un anno per sapere il diametro del grafo che contiene i film dell'anno inserito")
        x = int(input())
    else:
        print("########## Ricerca del diametro per l'anno: ",year)
        x = year
    CC = connected_component(x)
    stop_time()
    node = middle_node_of_2_sweep(CC)
    start_time()
    print("Calcolo eccentricità")
    i = nx.eccentricity(CC, v=node)
    stop_time()
    lb = i
    ub = 2*i
    print("Calcolo Frangia")
    start_time()
    targets = calculate_fringe(CC,node)
    stop_time()
    print("Calcolo diametro")
    start_time()
    while ub > lb:
        b_i = calculate_b_i(CC, targets, i)
        if max(lb, b_i) > 2*(i-1):
            break
        else:
            lb = max(lb, b_i)
            ub = 2*(i-1)
        i -= 1
    lb = max(lb,b_i)
    print("#################################")
    if saveOnFile:
        file = open("diameterResult.txt", "a+")
        to_write = "##########################\nTempo di esecuzione: " + stop_time(True) +"\nAnno: " + str(x) +"\nDiametro: " + str(lb) +"\n##################"
        file.write(to_write)
        file.close
    output = "##########################\nTempo di esecuzione: " + stop_time(True) +"\nAnno: " + str(x) +"\nDiametro: " + str(lb) +"\n##################"
    print(output)


def resolve_question_3():
    print("############### Ricerca attore con il massimo numero di collaborazioni ###############")
    max = 0
    max_id = 0
    start_time()
    for actor_id in actor_dic.values():
        # Prendiamo la lista dei film dove ha lavorato
        film_list = list(G.neighbors(actor_id))
        # Per ogni film contiamo il numero degli attori
        num = 0
        for film in film_list:
            actors_in_film = list(G.neighbors(film))
            num += len(actors_in_film) - 1
        if max < num:
            max = num
            max_id = actor_id
    stop_time()
    print("Attore con massimo numero di collaborazioni: ",reverse_actor.get(max_id), " Numero collaborazioni: ",max)
    print("###########################################################")
    return max_id,max


def resolve_question_4():
    global id
    global actor_dic
    global movie_dic
    global reverse_movie
    global reverse_actor
    global movie_actors_dic
    global edge_list
    global collaboration_list
    global G
    print('################## Creazione struttura dati contenente gli attori ##################')
    printRamUsage()
    print("Memory dump dei dizionari, liste e del grafo")
    del id
    del actor_dic
    del movie_dic
    del reverse_movie
    del edge_list
    del G
    printRamUsage()
    print("Creazione del grafo")
    start_time()
    simulated_graph = {}
    max_edge_peso = 0
    max_edge = 0
    for actors in movie_actors_dic.values():
        i = 1
        for node1 in range(len(actors)-1):
            for node2 in range(i,len(actors)):
                edge = (actors[node1],actors[node2])
                arco_peso = simulated_graph.get(edge)
                if arco_peso is not None:
                    simulated_graph.update({ edge: arco_peso + 1})
                    if max_edge_peso < (arco_peso + 1):
                        max_edge_peso = arco_peso + 1
                        max_edge = edge
                else:
                    simulated_graph.update({edge:1})
            i += 1


    stop_time()
    printRamUsage()
    print("Archi trovati: ",len(simulated_graph))
    print("Attori con massime collaborazioni: ", reverse_actor.get(max_edge[0]), reverse_actor.get(max_edge[1]))


# Il codice commentato costruisce il grafo per la risposta alla domanda 4, ma essendo che la memoria disponibile
# sui nostri dispositivi non è sufficiente questo codice non viene eseguito.
# def resolve_question_4():
#     global id
#     global actor_dic
#     global movie_dic
#     global reverse_movie
#     global reverse_actor
#     global movie_actors_dic
#     global edge_list
#     global collaboration_list
#     global G
#     print('################## Creazione struttura dati contenente gli attori ##################')
#     printRamUsage()
#     print("Memory dump dei dizionari, liste e del grafo")
#     del id
#     del actor_dic
#     del movie_dic
#     del reverse_movie
#     del edge_list
#     del collaboration_list
#     del G
#     del reverse_actor
#     printRamUsage()
#     print("Creazione del grafo")
#     start_time()
#     AG = nx.MultiGraph()
#     max_edge_peso = 0
#     max_edge = 0
#     for film_id,actors in list(movie_actors_dic.items()):
#         print(len(movie_actors_dic.keys()))
#         del movie_actors_dic[film_id]
#         print(len(movie_actors_dic.keys()))
#         i = 1
#         for node1 in range(len(actors)-1):
#             for node2 in range(i,len(actors)):
#                 try:
#                     if AG.has_edge(AG[node1],AG[node2]):
#                         AG[node1][node2]["weight"] = AG[node1][node2]["weight"] + 1
#                         if AG[node1][node2]["weight"] > max_edge_peso:
#                             max_edge_peso = AG[node1][node2]["weight"]
#                             max_edge = (node1, node2)
#                 except:
#                     AG.add_edge(node1,node2,weight=1)
#             i += 1
#
#
#     stop_time()
#     printRamUsage()
#     print(AG)
#     print("Attori con massime collaborazioni: ", reverse_actor.get(max_edge[0]), reverse_actor.get(max_edge[1]))



if __name__ == '__main__':
    data = loadData()
    # Costruzione dizionario
    # Con list comprehension
    create_graph(data)
    resolve_question_1()
    # for year in [1970,1980,1990,2000,2010,2020]:
    #     resolve_question_2(year,saveOnFile=True)
    # resolve_question_3()
    # resolve_question_4()


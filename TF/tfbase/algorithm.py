import json
import itertools
import pandas as pd
from math import radians, cos, sin, asin, sqrt
import networkx as nx
from heapq import heappush as push, heappop as pop
import heapq as pq 
import math
uri="https://raw.githubusercontent.com/Setsuke/AlgorithmComplexityProject/main/TP/poblaciones.csv"
url = "../data/poblaciones.csv"

def algorithm1(departamento):
    data = pd.read_csv(uri)
    data2 = data[data["DEPARTAMENTO"] == departamento]
    responsePath = []
    for i, row in data2.iterrows():
        responsePath.append({"idx": i,
                             "lat": float(row["LATITUD"]),
                             "lon": float(row["LONGITUD"])})

    return json.dumps(responsePath)

def algorithm():
    data = pd.read_csv(uri)
    responsePath = []
    for i, row in data.iterrows():
        responsePath.append({"idx": i,
                             "lat": float(row["LATITUD"]),
                             "lon": float(row["LONGITUD"])})

    return json.dumps(responsePath)

caminito = []

def haversine(row):
  lon1, lat1, lon2, lat2 = map(radians, [row["LongitudO"], row["LatitudO"], row["LongitudD"], row["LatitudD"]])

  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 
  r = 6371 
  distancia = c*r
  return distancia

def valid(aux,i):
  if aux != i and i['visited'] == False:
    return True
    
def backtracking(G, aux, inicio, cont):
  if cont == len(G):
    caminito.append({"cp":inicio,"lat":G.nodes[inicio]['Latitud'],"lon":G.nodes[inicio]['Longitud']})
    return caminito
  else:
    min = math.inf   
    G.nodes[aux]['visited'] = True   
    caminito.append({"cp":aux,"lat":G.nodes[aux]['Latitud'],"lon":G.nodes[aux]['Longitud']})
    for i in G.nodes:      
      if valid(G.nodes[aux],G.nodes[i]):
        pdist = G.edges[aux, i]['weight']
        if pdist < min:
          min = pdist
          aux = i
          cont+=1     
          backtracking(G, aux, inicio, cont)



def peru1():
    df = pd.read_csv(uri)
    df2 = df[df['DEPARTAMENTO']=='AYACUCHO']
    df2 = df2[["DEPARTAMENTO","DISTRITO","CENTRO POBLADO", "LATITUD", "LONGITUD"]]
    df2["CP"] = df2.index
    dftemp=df2["CP"]
    dftry=pd.DataFrame(data=dftemp)
    import itertools
    cps=df2['CP']
    list(itertools.permutations(cps,2))
    centros=df2['CENTRO POBLADO']
    list(itertools.permutations(centros,2))
    latitudes=df2['LATITUD']
    list(itertools.permutations(latitudes,2))
    longitudes=df2['LONGITUD']
    list(itertools.permutations(latitudes,2))

    combinacionesCentros = list(itertools.permutations(centros,2))
    combinacionesLatitudes = list(itertools.permutations(latitudes,2))
    combinacionesLongitudes = list(itertools.permutations(longitudes,2))
    combinacionesCps = list(itertools.permutations(cps,2))
    df3 = pd.DataFrame(combinacionesCentros,columns=['Origen','Destino'])
    df4 = pd.DataFrame(combinacionesLatitudes,columns=['LatitudO','LatitudD'])
    df4 = df4.apply(pd.to_numeric)
    df5 = pd.DataFrame(combinacionesLongitudes,columns=['LongitudO','LongitudD'])
    df5 = df5.apply(pd.to_numeric)
    dfx = pd.DataFrame(combinacionesCps,columns=['CPO','CPD'])
    dfx = dfx.apply(pd.to_numeric)
    df6=df3.join(df4)
    df6.join(df5)
    df7=df6.join(df5)
    dfz=df7.join(dfx)

    

    dfz["Distancia"] = dfz.apply(haversine,axis=1)
    df8=dfz[["Origen","Destino","Distancia","CPD","LatitudD","LongitudD"]]
    df9=df8.assign(IdDP=lambda x: x.CPD * 0 + 1)
    DEPARTAMENTO=df9.to_dict('index')

    dictionary = {}
    for i in DEPARTAMENTO:
        a = DEPARTAMENTO[i]['Origen']
        dictionary[a] =[]
    for i in DEPARTAMENTO:
        a = DEPARTAMENTO[i]['Origen']
        b = DEPARTAMENTO[i]['Destino']
        c = DEPARTAMENTO[i]['Distancia']
        d = DEPARTAMENTO[i]['CPD'] 
        midict = {'Destino':b,'Distancia':c,'CPD':d,'Latitud':DEPARTAMENTO[i]['LatitudD'],'Longitud':DEPARTAMENTO[i]['LongitudD']}
        dictionary[a].append(midict)
  
    
    adj = [[] for _ in range(len(dictionary))]

    Grafito = nx.Graph()

    i = -1
    vis = []
    orden = []

    for origen in dictionary.keys():
        a = origen
        orden.append(a)
        i = i + 1
        for destino_dict in dictionary[origen]:
            #for z,key in enumerate(destino_dict):
            #if key == 'CPD':
            #  codigo = key
            #else:
            b = destino_dict['Destino']
            c = destino_dict['Distancia']
            lat = destino_dict['Latitud']
            lon = destino_dict['Longitud']
            adj[i].append((b,c))
            Grafito.add_edge(a, b, weight=c)
            Grafito.nodes[b]['CPD'] = destino_dict['CPD']
            Grafito.nodes[b]['Latitud'] = destino_dict['Latitud']
            Grafito.nodes[b]['Longitud'] = destino_dict['Longitud']
    
    for n in Grafito.nodes:
        Grafito.nodes[n]['visited'] = False

    backtracking(Grafito, 'INQUE', 'INQUE', 0)
    responsePath = caminito


    return json.dumps(responsePath)

def prim(G, s): #2821
  for u in G.nodes:
    G.nodes[u]['visited'] = False
    G.nodes[u]['cost'] = math.inf
    G.nodes[u]['path'] = -1

  q = [(0, s)]#(0,2821)
  while q:
    _, u = pop(q) # 0, 2821
    if not G.nodes[u]['visited']:
      G.nodes[u]['visited'] = True
      for v in G.neighbors(u):
        if not G.nodes[v]['visited']:
          w = G.edges[u, v]['weight']
          if w < G.nodes[v]['cost']:
            G.nodes[v]['cost'] = w
            G.nodes[v]['path'] = u
            push(q, (w, v))

  path = []
  for u in G.nodes:
    path.append({'CP':G.nodes[u]['path'],'lat':G.nodes[u]['Latitud'],'lon':G.nodes[u]['Longitud']})
    if G.nodes[u]['cost'] == math.inf:
      G.nodes[u]['cost'] = 0

  return path

    
def peru2():
    df = pd.read_csv(uri)
    df2 = df[df['DEPARTAMENTO']=='LORETO']
    df2 = df2[["DEPARTAMENTO","DISTRITO","CENTRO POBLADO", "LATITUD", "LONGITUD"]]
    df2["CP"] = df2.index
    dftemp=df2["CP"]
    dftry=pd.DataFrame(data=dftemp)
    import itertools
    cps=df2['CP']
    list(itertools.permutations(cps,2))
    centros=df2['CENTRO POBLADO']
    list(itertools.permutations(centros,2))
    latitudes=df2['LATITUD']
    list(itertools.permutations(latitudes,2))
    longitudes=df2['LONGITUD']
    list(itertools.permutations(latitudes,2))

    combinacionesCentros = list(itertools.permutations(centros,2))
    combinacionesLatitudes = list(itertools.permutations(latitudes,2))
    combinacionesLongitudes = list(itertools.permutations(longitudes,2))
    combinacionesCps = list(itertools.permutations(cps,2))
    df3 = pd.DataFrame(combinacionesCentros,columns=['Origen','Destino'])
    df4 = pd.DataFrame(combinacionesLatitudes,columns=['LatitudO','LatitudD'])
    df4 = df4.apply(pd.to_numeric)
    df5 = pd.DataFrame(combinacionesLongitudes,columns=['LongitudO','LongitudD'])
    df5 = df5.apply(pd.to_numeric)
    dfx = pd.DataFrame(combinacionesCps,columns=['CPO','CPD'])
    dfx = dfx.apply(pd.to_numeric)
    df6=df3.join(df4)
    df6.join(df5)
    df7=df6.join(df5)
    dfz=df7.join(dfx)

    dfz["Distancia"] = dfz.apply(haversine,axis=1)
    df8=dfz[["Origen","Destino","Distancia","CPD","LatitudD","LongitudD"]]
    df9=df8.assign(IdDP=lambda x: x.CPD * 0 + 1)
    DEPARTAMENTO=df9.to_dict('index')

    dictionary = {}
    for i in DEPARTAMENTO:
        a = DEPARTAMENTO[i]['Origen']
        dictionary[a] =[]
    for i in DEPARTAMENTO:
        a = DEPARTAMENTO[i]['Origen']
        b = DEPARTAMENTO[i]['Destino']
        c = DEPARTAMENTO[i]['Distancia']
        d = DEPARTAMENTO[i]['CPD'] 
        midict = {'Destino':b,'Distancia':c,'CPD':d,'Latitud':DEPARTAMENTO[i]['LatitudD'],'Longitud':DEPARTAMENTO[i]['LongitudD']}
        dictionary[a].append(midict)
        Grafito = nx.Graph()

    i = -1
    vis = []
    orden = []

    for origen in dictionary.keys():
        a = origen
        orden.append(a)
        i = i + 1
        for destino_dict in dictionary[origen]:
            #for z,key in enumerate(destino_dict):
            #if key == 'CPD':
            #  codigo = key
            #else:
            b = destino_dict['Destino']
            c = destino_dict['Distancia']
            lat = destino_dict['Latitud']
            lon = destino_dict['Longitud']
            Grafito.add_edge(a, b, weight=c)
            Grafito.nodes[b]['CPD'] = destino_dict['CPD']
            Grafito.nodes[b]['Latitud'] = destino_dict['Latitud']
            Grafito.nodes[b]['Longitud'] = destino_dict['Longitud']
    

    responsePath = prim(Grafito,'ALIANZA')
    

    return json.dumps(responsePath)


def peru3():
    df = pd.read_csv(uri)
    df2 = df[df['DEPARTAMENTO']=='LAMBAYEQUE']
    df2 = df2[["DEPARTAMENTO","DISTRITO","CENTRO POBLADO", "LATITUD", "LONGITUD"]]
    df2["CP"] = df2.index
    dftemp=df2["CP"]
    dftry=pd.DataFrame(data=dftemp)
    import itertools
    cps=df2['CP']
    list(itertools.permutations(cps,2))
    centros=df2['CENTRO POBLADO']
    list(itertools.permutations(centros,2))
    latitudes=df2['LATITUD']
    list(itertools.permutations(latitudes,2))
    longitudes=df2['LONGITUD']
    list(itertools.permutations(latitudes,2))

    combinacionesCentros = list(itertools.permutations(centros,2))
    combinacionesLatitudes = list(itertools.permutations(latitudes,2))
    combinacionesLongitudes = list(itertools.permutations(longitudes,2))
    combinacionesCps = list(itertools.permutations(cps,2))
    df3 = pd.DataFrame(combinacionesCentros,columns=['Origen','Destino'])
    df4 = pd.DataFrame(combinacionesLatitudes,columns=['LatitudO','LatitudD'])
    df4 = df4.apply(pd.to_numeric)
    df5 = pd.DataFrame(combinacionesLongitudes,columns=['LongitudO','LongitudD'])
    df5 = df5.apply(pd.to_numeric)
    dfx = pd.DataFrame(combinacionesCps,columns=['CPO','CPD'])
    dfx = dfx.apply(pd.to_numeric)
    df6=df3.join(df4)
    df6.join(df5)
    df7=df6.join(df5)
    dfz=df7.join(dfx)

    dfz["Distancia"] = dfz.apply(haversine,axis=1)
    df8=dfz[["Origen","Destino","Distancia","CPD","LatitudD","LongitudD"]]
    df9=df8.assign(IdDP=lambda x: x.CPD * 0 + 1)
    DEPARTAMENTO=df9.to_dict('index')

    dictionary = {}
    for i in DEPARTAMENTO:
        a = DEPARTAMENTO[i]['Origen']
        dictionary[a] =[]
    for i in DEPARTAMENTO:
        a = DEPARTAMENTO[i]['Origen']
        b = DEPARTAMENTO[i]['Destino']
        c = DEPARTAMENTO[i]['Distancia']
        d = DEPARTAMENTO[i]['CPD'] 
        midict = {'Destino':b,'Distancia':c,'CPD':d,'Latitud':DEPARTAMENTO[i]['LatitudD'],'Longitud':DEPARTAMENTO[i]['LongitudD']}
        dictionary[a].append(midict)
    
    Grafito = nx.Graph()
  
    adj = [[] for _ in range(len(dictionary))]

    i = -1
    vis = []
    orden = []
    def validDFS(nodo:str):
      if nodo in vis:
        return False
      else:
        return True
    arr = []
    def DFS(nodito: str, peso: float):
      vis.append(nodito)

      index = list(orden).index(nodito)
      #Busco su index para recorrer sus vecinos

      q = [] # q es la cola soporte de heapq
      for e, w in adj[index]:
        pq.heappush(q, (w, e))
      
      while len(q) > 0 :
        n,v = pq.heappop(q)
        if validDFS(v):
          arr.append({'CP':Grafito.nodes[v]['CPD'],'lat':Grafito.nodes[v]['Latitud'],'lon':Grafito.nodes[v]['Longitud']})
          DFS(v, n)
          break

    for origen in dictionary.keys():
      a = origen
      orden.append(a)
      i = i + 1
      for destino_dict in dictionary[origen]:
        #for z,key in enumerate(destino_dict):
          #if key == 'CPD':
          #  codigo = key
          #else:
        b = destino_dict['Destino']
        c = destino_dict['Distancia']
        lat = destino_dict['Latitud']
        lon = destino_dict['Longitud']
    
        Grafito.add_edge(a, b, weight=c)
        adj[i].append((b,c))
        Grafito.nodes[b]['CPD'] = destino_dict['CPD']
        Grafito.nodes[b]['Latitud'] = destino_dict['Latitud']
        Grafito.nodes[b]['Longitud'] = destino_dict['Longitud']

    responsePath=[]
    DFS('ALAMO',0)
    responsePath=arr
    return json.dumps(responsePath)
      

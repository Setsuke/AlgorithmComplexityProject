import math
import netwowkx
#obtamos dfs por que es bactacking
#Listas de adyacencia para cada nodo

#def almacenado(cities):


#def valid(string:tour,float:c):
    #que coja la menor distancia
    #que no agarre la distancia de la que viene
#    cities[r][c]

#minimun = math.inf
def build_path(cities):
    adj = [[] for _ in range(len(cities))]
    i=-1
    vis = {}
    dis= {}
    for origen in cities.keys():
        a = origen
        vis[a] =False
        dis[a]=math.inf
        i = 1+1
        for destino in cities[origen].keys():
            b = destino
            c = cities[origen][destino]
            adj[i].append((b,c))
   

    c= start
    def dfs(n: int, adj: list):
    vis[c] = True
    for origen in adj[]:
        #estoy extrayendo en la poscion v

        
    #    for 





 #marco como visitado
 #a los que no he visitado lazo DFS
 #el key a donde va y lo almaceno
 #saco el peso y lo almacen
 # for origen in cities.keys():
 #
 #     vis[origen] = True
 #     for destino in cities[origen].key():

 #  return minimun              




if __name__=='__main__':
    cities = {
        'RV': {'S': 195, 'UL': 86, 'M': 178, 'BA': 180, 'Z': 91},
        'UL': {'RV': 86, 'S': 107, 'N': 171, 'M': 123},
        'M': {'RV': 178, 'UL': 123, 'N': 170},
        'S': {'RV': 195, 'UL': 107, 'N': 210, 'F': 210, 'MA': 135, 'KA': 64},
        'N': {'S': 210, 'UL': 171, 'M': 170, 'MA': 230, 'F': 230},
        'F': {'N': 230, 'S': 210, 'MA': 85},
        'MA': {'F': 85, 'N': 230, 'S': 135, 'KA': 67},
        'KA': {'MA': 67, 'S': 64, 'BA': 191},
        'BA': {'KA': 191, 'RV': 180, 'Z': 85, 'BE': 91},
        'BE': {'BA': 91, 'Z': 120},
        'Z': {'BA': 120, 'BE': 85, 'RV': 91}
    }

    build_path(cities)
 




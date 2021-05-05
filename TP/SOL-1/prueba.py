import heapq as pq #priority queue


def DFS(nodito: str, peso: float):
  vis.append(nodito)
  
  i = i + peso

  index = list(orden).index(nodito)
  #Busco su index para recorrer sus vecinos

  q = [] # q es la cola soporte de heapq
  for e, w in adj[index]:
    print(nodito)
    print(str(e)+' '+str(w))
    print('--------')
    pq.heappush(q, (w, e))
  
  while len(q) > 0 :
    n,v = pq.heappop(q)
    if valid(v):
      DFS(v, n)
      break
 
# Dijkstra
## Graph Notation
- s - The start vertex
- d[v] - The current shortest path distance from s to v
- $\Pi$[v] - The predecessor of v on the shortest path from s to v
- $\delta$[u, v] - The actual shortest path length from u to v
- w(u, v) - The weight function w gives us the weight of the path going from u to v, given that (u,v) $\in$ E, the set of edges

## Relaxation of Edges
We “relax” an edge if we find a shorter path to the vertex the edge is pointing to than we currently know.

We look at an edge (u, v). If we find that the path from u to v is shorter than d[v], we update the value d[v] to be this new shorter path. We keep doing this for all edges and eventually, we end up with the shortest path to every vertex v starting from the start vertex s.

~~~
Relax(u, v, w):
    if d[v] > d[u] + w(u, v):
        d[v] = d[u] + w(u, v)
        predecessor[v] = u
~~~

The algorithm we talked about in the last lecture just picked edges to relax randomly, but that algorithm does very poorly complexity-wise. Keeping the general idea the same, if we are a little smarter about how we pick the edges we want to relax, we get a much better algorithm (Dijkstra or Bellman-Ford).

## The General Algorithm
The general algorithm works only for directed acyclic graphs which may or may not have negative edges. The algorithm works in 2 main steps

1. Sort the graph topologically using depth first search.
2. If we use DFS to sort topologically, we can say that a shortest path exists from u to v iff u comes before v in the ordering that DFS gives us.
3. Represent the sorted graph linearly and choose a start vertex.
4. Go through the sorted linear graph in order from left to right, relax each edge you encounter as you go, and by the end, you have found all the shortest paths.
5. Every vertex to the left of s gets a (s, v) of .

The depth first search takes O(V + E) time, and we only look at each edge once, which takes O(E) time, so our general algorithm takes O(V + E) time.

## Dijkstra's Algorithm
Dijkstra is a greedy algorithm, and it only works for undirected graphs without negative edges.
Dijkstra starts with a vertex, relaxes all the edges emanating from it, and assumes that the shortest path to that vertex has been found.

~~~
Dijkstra(G, w, s):
    solved = set() # S contains the set of solved vertices
    Q = priority_queue()
    Q.add(V) # Q contains the set of vertices of the graph
    d = dict() # d will contain the d values of all the vertices as we go on relaxing them

    while Q:
        # While there are still elements in Q, do
        u = extract_min(Q) # return the element with the lowest priority in Q and remove it from Q.
        solved.add(u) # Assume that u has been solved
        for v in Adj[u]:
            relax(u, v, w)
~~~
{: .language-python}

The priority queue Q will be ordered by the d values in the dictionary d.
We implement the priority queue using a min-heap, and calculating the cost of operations required in the implementation above gives us a complexity of $\Theta(V \cdot log\,V+E \cdot log\,V)$. If we implement the priority queue using a fibonacci heap, we get a complexity of $\Theta(V \cdot log\,V+E)$.

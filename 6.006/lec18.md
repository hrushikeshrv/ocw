# Speeding Up Dijkstra
We can perform some optimizations to our dijkstra implementation to improve the average runtime. The worst case complexity remains the same, but the average case complexity goes down.

## Optimization 1 - Early Stopping
We add one check to vanilla dijkstra -

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
        # t is our destination vertex
        if u == t:
            return
~~~
{: .language-python}

If you know what the destination vertex is, you don’t need to keep relaxing edges after you are done with the destination vertex. So you return if you are done with the destination vertex.

## Optimization 2 - Bidirectional Search
Instead of the search for shortest paths going in just one direction, we search for shortest paths in both directions. We do one step of forward search starting from s, then we do one step of backward search starting from t. In each step we do just what dijkstra usually does. We stop when we find a vertex that has been searched both forwards and backwards.

To implement this search, we need to maintain 3 more data structures. We have Q, d[v], and $\Pi$ for the forward search like we did before, but now we also have another Q, d[v], and $\Pi$ for the backward search. We call them Q<sub>f</sub> and Q<sub>b</sub>, d<sub>f</sub> and d<sub>b</sub>, and $\Pi$<sub>f</sub> and $\Pi$<sub>b</sub>. Q<sub>f</sub> is the processing queue for vertices going in the forward direction, Q<sub>b</sub> is the same going in the backward direction. $\Pi$<sub>f</sub> is the predecessor relationship dictionary going in the forward direction and $\Pi$<sub>b</sub> is the same going in the backward direction. d<sub>f</sub>[v] is the length of the current shortest path to v in the forward direction and d<sub>b</sub>[v] is the same for the backward direction.

Once we terminate, i.e. find a node t that has been processed both ways, we start to find the shortest paths. The shortest path might not always be the path joining s to w to t. Once we terminate, we must check all the vertices who have a finite d<sub>b</sub>[v] and d<sub>f</sub>[v] value, and check to see if they form a shorter path than s $\to$ w $\to$ t.

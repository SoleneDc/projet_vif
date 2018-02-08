#old    
    def parcours_k_chemins(self, k=1):
        visited = []
        L = []
        T = []
        def visit(noeud, L):
            visited.append(noeud)
            L += zip([noeud]*len(list(self.G.adj[noeud])), list(self.G.adj[noeud]))
        visit(1, L)
        while L :
            nv = L.pop(len(L)-1)
            if nv not in visited:
                T.append(nv)
                visit(nv[1], L)
        return T


#new

def parcours_k_chemins(self, k=7):
    buffer = []
    L = []
    T = {}
    i = 1
    
    def visit(noeud, L, T, i):
        voisins = list(self.G.adj[noeud])
        L += zip([noeud]*len(voisins), voisins)
        if len(voisins) > 1:
            buffer = list(T[i])
        elif len(voisins) == 0 and L[len(L)-1][0] != 1:
            i += 1
            T[i] += buffer
        elif len(voisins) == 0 and L[len(L)-1][0] == 1:
            i += 1
            
    visit(1, L, T, i)
    while L :
        nv = L.pop(len(L)-1)
        T[i].append(nv)
        visit(nv[1], L, T, i)
    return T
# Author: Edison Murairi
# Date: Oct. 19th, 2022
import numpy as np
import networkx as nx

#print("this is the new one")
def F(i,j, z):

    res = 0
    for p in z:
        for k in range(len(p)):

            if int(p[i]) == 1 and int(p[j]) == 1:
                res += 1
            if int(p[i]) == 0 and int(p[j]) == 1:
                res += 0
            if int(p[i]) == 1 and int(p[j]) == 0:
                res -= 1

    return res

def aggregateF(permuted, z, n):

    res = 0
    for i in range(n-1):
        res += F(permuted[i], permuted[i+1], z)
    return res

def make_weighted_graph(z,n):

    G = nx.DiGraph()
    for i in range(n):
        for j in range(i+1, n):
            G.add_edge(i, j, weight=F(i,j,z))
            G.add_edge(j, i, weight=F(j,i,z))
    return G

def make_graph(z,n):

    G = nx.DiGraph()
    for i in range(n):
        for j in range(i+1, n):
            if F(i,j,z) > F(j,i,z):
                G.add_edge(i,j)
            else:
                G.add_edge(j,i)
    return G

#coding=utf8
__author__ = 'Administrator'

import igraph

# noted that scipy is just a wrapper for numpy, all the function used in numpy can also be used in scipy and you can change the namespaces
from scipy import linalg
from scipy import matrix

def eig():
    g=igraph.Graph(n=14,directed=False)
    g.add_edges([(1,2),(1,3),(1,4),(1,10)])
    g.add_edges([(2,3)])
    g.add_edges([(3,4)])
    g.add_edges([(4,5),(4,6)])
    g.add_edges([(5,6),(5,7),(5,8)])
    g.add_edges([(6,7),(6,8)])
    g.add_edges([(7,8),(7,9)])
    g.add_edges([(10,11),(10,12),(10,13)])
    g.add_edges([(11,12),(11,13)])
    g.add_edges([(12,13)])
    g.delete_vertices(g.vs[0])
    return g
    
def get_eigvector(g):
    '''
    Return the eigenvector of the second smallest eigenvalue
    Noted that the return type is numpy.narray
    '''
    m=matrix(g.laplacian())
    # v is the eigenvalue and d is the eigen matrix
    v,d=linalg.eig(m)
    # this is the desired eigenvector but i dont know why now
    # sort the eigen value and retrieve the second small one
    minList=[0,1]
    func=lambda x,y:cmp(v[x],v[y])
    minList.sort(cmp=func)
    for idx,eigv in enumerate(v[2:]):
        if eigv<v[minList[1]]:
            minList[1]=idx
            minList.sort(cmp=func)
    print d[:,minList[1]]
    return d[:,minList[1]]

def igraph_eig_vector(g):
    return g.community_leading_eigenvector()

if __name__=='__main__':
    pass
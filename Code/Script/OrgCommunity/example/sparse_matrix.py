#coding=utf8
__author__ = 'Administrator'

import igraph

# noted that scipy is just a wrapper for numpy, all the function used in numpy can also be used in scipy and you can change the namespaces
from scipy import linalg
from scipy.sparse import coo_matrix

from time import clock

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
    
def eig_figure1():
    g=igraph.Graph(n=10,directed=False)
    g.add_edges([(1,2),(1,3),(1,4)])
    g.add_edges([(2,3)])
    g.add_edges([(3,4)])
    g.add_edges([(4,5),(4,6)])
    g.add_edges([(5,6),(5,7),(5,8)])
    g.add_edges([(6,7),(6,8)])
    g.add_edges([(7,8),(7,9)])
    g.delete_vertices(g.vs[0])
    return g
    
def eig_figure1_weighted():
    g=igraph.Graph(n=10,directed=False)
    g.add_edges([(1,2),(1,3),(1,4)])
    g.add_edges([(2,3)])
    g.add_edges([(3,4)])
    g.add_edges([(4,5),(4,6)])
    g.add_edges([(5,6),(5,7),(5,8)])
    g.add_edges([(6,7),(6,8)])
    g.add_edges([(7,8),(7,9)])
    g.delete_vertices(g.vs[0])
    g.es['weight']=[0.7,0.7,0.7,0.7,0.7,0.2,0.2,0.8,0.8,0.8,0.8,0.8,0.8,0.1]
    return g
    
def get_matrix(g):
    from numpy import array
    vecCount=len(g.vs)
    row=[]
    col=[]
    data=[]
    for i in g.vs:
        row.append(i.index)
        col.append(i.index)
        data.append(i.degree())
        pass
    for e in g.es:
        row.append(e.source)
        col.append(e.target)
        data.append(-1)
        row.append(e.target)
        col.append(e.source)
        data.append(-1)
    row=array(row)
    col=array(col)
    data=array(data)
    m=coo_matrix((data,(row,col)),shape=(vecCount,vecCount),dtype='float32')
    return m

    
def largest_component(g):
    '''
    actually I want return a graph
    '''
    vc=g.components()
    return vc.giant()
    
def get_eigvector(m):
    '''
    Return the eigenvector of the second smallest eigenvalue
    Noted that the return type is numpy.narray
    '''

    # v is the eigenvalue and d is the eigen matrix
    from scipy.sparse import linalg
    v,d=linalg.eigsh(A=m,k=2,which='SA')

def build_vertex_clustering(g):
    membeship=[0,0,0,0,1,1,1,1,1,2,2,2,2]
    from igraph.clustering import VertexClustering
    vc=VertexClustering(g,membership)
    return vc
    
def igraph_eig_vector(g):
    return g.community_leading_eigenvector()
    
def mem_test():
    '''
    this function aim to find how many elements can be stored in the matrix
    I mean if the matrix is not sparse, sometimes it can be stored easily
    '''
    from scipy import matrix
    l=[0]*10000
    l1=[l]*10000
    m=matrix(l1)
    return m
    

if __name__=='__main__':
    g=eig_figure1()
    print g.community_fastgreedy().as_clustering().q
    
    g1=eig_figure1_weighted()
    print g1.community_fastgreedy(weights='weight').as_clustering().q
    pass
#coding=utf-8
__author__ = 'Administrator'

from igraph import *

def simple_example():
    es=[(1,5),(2,4),(1,7)]
    g=Graph(edges=es,directed=False)

    print summary(g)
    plot(g)


def simple_example2():
    '''
    Undirected graph (|V| = 7, |E| = 8)
    Undirected graph (|V| = 3, |E| = 3)
    '''
    g=Graph(n=7,directed=False)
    for v in g.vs:
        v['name']=str(v.index)
    g.add_edges([(0,1),(0,2),(0,3),(0,4),(0,5),(1,3),(1,5),(3,5)])
    print g

    odd_seq=g.vs.select(lambda vertex:vertex.index%2==1)

    g1=g.subgraph(odd_seq)
    print g1

    return g

def simple_example3():
    x=5
    g=Graph(n=x,directed=False)
    for i in range(x):
        g.vs[i]['name']=str(i)
    print g
    return g

def simple_example4():
    x=5
    g=Graph(n=x,directed=False)
    for i in range(x):
        g.vs[i]['name']=str(i)

    for i in range(x-1):
        g.add_edges((i,i+1))
    print g
    return g

def simple_example5():
    g=Graph(n=0,directed=False)
    g.add_vertex(name='kira',age=12,gender='male')

    #how to refer a vertex by its name
    vertexSeq=g.vs.select(name='kira')
    return g

def simple_example6():
    g=Graph(n=200000,directed=False)
    f2=open('E:\\Graduation\\Data\\edges_utf.csv')
    edge_count=0
    edge_list=[]
    for line in f2:
        l=line.strip('﻿ ').split(',')
        edge_list.append((int(l[0])-1,int(l[1])-1))

    f2.close()
    g.add_edges(edge_list)

    print 'add %s edges totally'%g.ecount()
    return g


if __name__=='__main__':
    simple_example6()
    pass

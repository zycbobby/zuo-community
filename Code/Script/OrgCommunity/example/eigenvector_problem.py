#coding=utf-8
__author__ = 'Administrator'

'''
In this file, we are going to solve the eigen vector problem by using the numerical method
'''

import sparse_matrix as sc

def solve(matrix):
    pass

def compute_modularity_matrix(g):
    '''
    aim to compute modularity matrix
    return a scipy sparse matrix
    '''
    from numpy import array
    from scipy.sparse import coo_matrix
    vecCount=len(g.vs)
    edgeCount=float(len(g.es))

    # first compute the adjmatrix
    row=[]
    col=[]
    data=[]
    for e in g.es:
        row.append(e.source)
        col.append(e.target)
        data.append(1)
        row.append(e.target)
        col.append(e.source)
        data.append(1)
    row=array(row)
    col=array(col)
    data=array(data)
    adj=coo_matrix((data,(row,col)),shape=(vecCount,vecCount),dtype='float64').asformat('csr')
    pass

    # then compute the P matrix
    row=[]
    col=[]
    data=[]
    for rIndex in xrange(vecCount):
        rdegree=g.vs[rIndex].degree()
        if rdegree==0:
            continue

        for cIndex in xrange(rIndex,vecCount):
            cdegree=g.vs[cIndex].degree()
            if cdegree==0:
                continue
            else:
                if cIndex==rIndex:
                    p=(rdegree*cdegree)/(2*edgeCount)
                    row.append(rIndex)
                    col.append(cIndex)
                    data.append(p)
                else:
                    p=(rdegree*cdegree)/(2*edgeCount)
                    row.append(rIndex)
                    col.append(cIndex)
                    data.append(p)
                    row.append(cIndex)
                    col.append(rIndex)
                    data.append(p)
                    pass
    row=array(row)
    col=array(col)
    data=array(data)
    p=coo_matrix((data,(row,col)),shape=(vecCount,vecCount),dtype='float64').asformat('csr')
    return adj-p

def write_matrix(m):
    f=open('test.matrix','w')
    for x in range(m.shape[0]):
        for y in range(m.shape[1]):
            f.write('%1.6f '%m[x,y])
        f.write('\n')
    f.close()
	
def power_method(m):
	import scipy
	length=m.shape[0]
	v=scipy.array([1.0/length]*length)

if __name__=='__main__':
    g=sc.eig_figure1()
    m=compute_modularity_matrix(g)
    #write_matrix(m)
    pass

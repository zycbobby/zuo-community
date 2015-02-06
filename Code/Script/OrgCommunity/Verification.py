# coding=utf-8

# Author:Zuozuo

'''
this module aim to verify that my community structure is non-trivial
'''

import SQLDao
import pickle
import igraph
import math
import random
import copy
from ExtractContentEdge import ContentEdgeExtractorBaseRoutine

class Verify(object):

    def __init__(self, base_dir,expr_dir, master_id):
        '''
        read the graph into the memory
        '''
        self.base_dir=base_dir
        self.expr_dir=expr_dir
        
        self.w1=float(SQLDao.ce.properties['w1'])
        self.w2=float(SQLDao.ce.properties['w2'])
        self.w3=float(SQLDao.ce.properties['w3'])
        self.criterion=float(SQLDao.ce.properties['sim_criterion'])
        
        self.master_id=master_id
        
        self._load_user_relation_pickle(master_id)
        self._load_user_content_pickle(master_id)
        
        # fulfill the content graph
        self._fulfill_content_graph(0.3)
        
        pass
    
    def _fulfill_content_graph(self,sim):
        '''
        since the edge of the content graph is not enough
        we have to add more edge to the graph
        '''
        # delete all edges
        self.cg.delete_edges(None)
        
        # rebuild the edges
        cebr=ContentEdgeExtractorBaseRoutine(self.base_dir,self.expr_dir)
        edges=[]
        weights=[]
        for i,vi in enumerate(self.cg.vs):
            for j in range(i+1,len(self.cg.vs)):
                vj=self.cg.vs[j]
                h1,h2,h3=cebr.compute_similarity(vi,vj)
                similarity=self.w1*h1+self.w2*h2+self.w3*h3
                if similarity>sim:
                    edges.append((i,j))
                    weights.append(similarity)
                pass
                
        self.cg.add_edges(edges)
        self.cg.es['weight']=weights
    
    
    def _load_user_relation_pickle(self,uid):
        '''
        given a uid, load uid.pickle, which should contain 
        relation edges and the user content feature in the node
        '''
        f=open(self.base_dir+self.expr_dir+'%s_relation.pickle'%uid)
        self.rg=pickle.load(f)
        f.close()
    
    def _load_user_content_pickle(self,uid):
        '''
        given a uid, load uid.pickle, which should contain 
        relation edges and the user content feature in the node
        '''
        f=open(self.base_dir+self.expr_dir+'%s_content.pickle'%uid)
        self.cg=pickle.load(f)
        f.close()

    #
    def Motivate_Once(self,graph,p):
        print 'handling p=%s'%p
        if not graph.is_weighted():
            vc1=graph.community_leading_eigenvector()
        else:
            vc1=graph.community_fastgreedy(weights='weight')
            vc1=vc1.as_clustering()

        graph_p=Verify.Perturbate(graph,p)

        if not graph_p.is_weighted():
            vc2=graph_p.community_leading_eigenvector()
        else:
            vc2=graph_p.community_fastgreedy(weights='weight')
            vc2=vc2.as_clustering()

        s1=self.partition_similarity(vc1,vc2)

        vc3=Verify.Build_random_clustering(vc1)
        vc4=Verify.Build_random_clustering(vc2)
        s2=self.partition_similarity(vc3,vc4)

        s=s1-s2


    def Motivate(self,graph,filename):
        '''
        '''
        f=open(self.base_dir+self.expr_dir+filename,'w')
        
        p_list=[x*1.0/100 for x in range(0,101,2)]
        
        
        s1_list=[]
        s2_list=[]
        s_list=[]
        
        if not graph.is_weighted():
            vc1=graph.community_leading_eigenvector()
        else:
            vc1=graph.community_fastgreedy(weights='weight')
            vc1=vc1.as_clustering()
        
        
        for p in p_list:        
            print 'handling p=%s'%p
            graph_p=Verify.Perturbate(graph,p)
            
            if not graph_p.is_weighted():
                vc2=graph_p.community_leading_eigenvector()
            else:
                vc2=graph_p.community_fastgreedy(weights='weight')
                vc2=vc2.as_clustering()

            s1=self.partition_similarity(vc1,vc2)
            
            vc3=Verify.Build_random_clustering(vc1)
            vc4=Verify.Build_random_clustering(vc2)
            s2=self.partition_similarity(vc3,vc4)
            
            s=s1-s2
            
            s1_list.append(s1)
            s2_list.append(s2)
            s_list.append(s)
        
        
        for s1 in s1_list:
            f.write('%s\t'%s1)
        
        f.write('\n')
        
        
        for s2 in s2_list:
            f.write('%s\t'%s2)
        
        f.write('\n')
        
        cumulative=0.0
        for i in range(1,len(s_list)):
            cumulative+=(s_list[i]+s_list[i-1])*0.02/2
            
        print cumulative
        for s in s_list:
            f.write('%s\t'%s)
        
        f.write('\n')
        
        f.close()
        
    @classmethod
    def Perturbate(cls,graph, p):
        '''
        move the edge according to the probability of p
        '''
        nodes_count=len(graph.vs)
        g=graph.copy()
        original_edges_set=set(map(lambda x:(x.source,x.target),g.es))

        de_edges_set=set()
        #ad_edges_set=set()
        ad_edges_dict=dict()
        for e in g.es:
            if random.random()<p:
                src=random.randint(0,nodes_count-2)
                tar=random.randint(src+1,nodes_count-1)

                while (src,tar) in set(ad_edges_dict.keys()).union(original_edges_set-de_edges_set):
                    src=random.randint(0,nodes_count-2)
                    tar=random.randint(src+1,nodes_count-1)

                de_edges_set.add((e.source,e.target))

                if not g.is_weighted():
                    ad_edges_dict[(src,tar)]=1
                else:
                    ad_edges_dict[(src,tar)]=e['weight']

        if not g.is_weighted(): #rg
            g.delete_edges(list(de_edges_set))
            g.add_edges(ad_edges_dict.keys())
        else: #cg
            g.delete_edges(list(de_edges_set))
            start_from=len(g.es)
            g.add_edges(ad_edges_dict.keys())

            for i in range(start_from,len(g.es)):
                e=g.es[i]
                e['weight']=ad_edges_dict[(e.source,e.target)]
            pass
            
        assert len(g.es)==len(graph.es)
        
        return g
        
    @classmethod
    def Build_random_clustering(cls, vc):
        '''
        build a vertex clustering according to the vc which is input
        the output of the vc_gen has the same number of nodes in each community
        '''
        nodes_count=vc.n
        l=vc.membership
        random.shuffle(l)
        return igraph.VertexClustering(vc.graph,l)
        
        
    def partition_similarity(self,A,B):
        '''
        I(A,B)=...
        A and B are two vertex clustering
        '''
        N=self.compute_confusion_matrix(A,B)
        
        
        # TODO: I dont think it is correct since the unit has some problem
        # NSum=Verify.SumMatrix(N)
        NSum=A.n
        
        total=0.0
        for i in range(N.shape[0]):
            for j in range(N.shape[1]):
                if N[i,j]!=0:
                    b=sum(N[i,:])*sum(N[:,j])
                    a=(N[i,j]*NSum)*1.0/b
                    total+=N[i,j]*math.log(a)
                
        total*=-2

        fraction=0.0
        for i in range(N.shape[0]):
            fraction+=sum(N[i,:])*math.log(sum(N[i,:])*1.0/NSum)
            
        for j in range(N.shape[1]):
            fraction+=sum(N[:,j])*math.log(sum(N[:,j])*1.0/NSum)
            
        return total/fraction
            
    
    
    @classmethod
    def SumMatrix(cls,m):
        assert isinstance(m,igraph.datatypes.Matrix)
        total=0
        for i in range(m._nrow):
            total+=sum(m[i,:])
        return total
    
    def compute_confusion_matrix(self,A,B):
        assert isinstance(A,igraph.VertexClustering)
        assert isinstance(B,igraph.VertexClustering)
        
        ndata=igraph.datatypes.Matrix.Zero((len(A),len(B)))
        
        for i in range(len(A)):
            for j in range(len(B)):
                g1=[idx for idx,community_id in enumerate(A.membership) if community_id==i]
                g2=[idx for idx,community_id in enumerate(B.membership) if community_id==j]
                s1=set(g1)
                s2=set(g2)
                ndata[i,j]=len(s1.intersection(s2))
        
        return ndata 
        
if __name__=='__main__':
    uid=1197161814
    v=Verify(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'],uid)

    #for i in range(20):
    #    v.Motivate(v.rg,'rg_significance_%s.txt'%i)
    
    for i in range(20):
        v.Motivate(v.cg,'cg_significance_%s.txt'%i)

    pass

if __name__=='__main__2':
    uid=1197161814
    v=Verify(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'],uid)
    v.Motivate_Once(v.cg,0.18)
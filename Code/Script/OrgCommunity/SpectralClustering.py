#coding=utf-8
import pickle
import SQLDao

__author__ = 'Administrator'

'''
Input, an object of igraph.Graph
1.  transform to laplacian matrix()
2.  compute eigenvector for the laplacian matrix(numpy)
3.  use orange to cluster different
'''
from util import Debugger as d
import FSDao
from scipy import matrix
from scipy.sparse import coo_matrix
from scipy.sparse import linalg
import gc
import orange
import Orange

class SoftIndicator(object):
    '''
    Noted that the input of this class is a undirected graph
    '''

    def __init__(self,expr_dir,graph_pickle_filename):
        '''
        load the graph file from the file system
        '''
        self.expr_dir=expr_dir
        self.graph_pickle_filename=graph_pickle_filename
        print 'loading graph pickle from %s'%expr_dir+graph_pickle_filename
        f=open(expr_dir+graph_pickle_filename,'rb')
        self.g=pickle.load(f)
        f.close()
        print 'loaded graph object(undirected) from file system'
        if self.g.is_directed():
            self.g=self.g.as_undirected()
            print 'transform graph to undirected'
        pass

    def iGraph_CommunityDiscovery(self, step=False):
        '''
        discover community in the relation graph, it takes time
        1. compute the vertexClustering
        2. serialize the vertexClustering

        step to see whether this function start from itself
        '''
        # why I serialize the vertexClustering:
        # even though I compute eigenvector myself, I am forced to construct vertexClustering myself
        self.vertex_clustering=d.trace(self.g.community_leading_eigenvector)()
        print 'modularity is %s'%self.vertex_clustering.modularity
        # print self.vertex_clustering.membership
        print 'finish find community_leading_eigenvector'
        FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['vertex_clustering_file_name'],self.vertex_clustering)
        pass

    def leading_eigen_vector(self):
        '''
        I would like to implement leading eigenvector methodology myself, which a critical challenge is the result should be totally the same with igraph
        community_leading_eigenvector
        '''
        import Queue
        import igraph
        membership=[0]*len(self.g.vs)
        vc=igraph.clustering.VertexClustering(self.g, membership)
        max_com_label=0
        q=Queue.Queue()
        q.put(0)
        max_modularity=vc.modularity

        # begin split iteratively until no split can increase the modularity
        while q.qsize()>0:
            cur_label=q.get()
            print 'cur label:%s, qsize: %s'%(cur_label,q.qsize())
            vertex_list=[idx for idx,com_label in enumerate(vc.membership) if com_label==cur_label]
            graph_to_split=self.g.subgraph(vertex_list)
            mod_matrix=self.compute_modularity_matrix(graph_to_split)
            gc.collect()
            eig=self.compute_largest_eigenvector(mod_matrix)
            # positive index and negative index
            if eig[0]>0:
                positive_index=[vertex_list[idx] for idx,v in enumerate(eig) if v>0]
                negative_index=[vertex_list[idx] for idx,v  in enumerate(eig) if v<=0]
            else:
                positive_index=[vertex_list[idx] for idx,v in enumerate(eig) if v<=0]
                negative_index=[vertex_list[idx] for idx,v  in enumerate(eig) if v>0]

            # noted that there are no set method for membership setting
            new_membership=vc.membership
            # positive index element keep the cur_label

            # negative index element use the max_label+1

            for idx in negative_index:
                new_membership[idx]=max_com_label+1
            vc_temp=igraph.clustering.VertexClustering(self.g, new_membership)
            # print 'new_membership:%s'%vc_temp.membership
            print 'old modularity: %s, new modularity: %s\n'%(vc.modularity,vc_temp.modularity)
            if vc_temp.modularity>vc.modularity:
                vc=vc_temp
                q.put(cur_label)
                q.put(max_com_label+1)
                max_com_label=max_com_label+1
            else:
                pass
            pass

        self.vertex_clustering=vc
        # print self.vertex_clustering.membership
        print 'writing vertex_clustering'
        FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['vertex_clustering_file_name'],self.vertex_clustering)
        print 'finished writing vertex_clustering'
        pass

    def save_adjacency_matrix_to_mat(self):
        '''
        this function aim to save the ajacency matrix to the mat file that can be used by matlab
        '''
        d=self.g.get_adjacency(type=2);
        from scipy import matrix
        from scipy.io import savemat
        adj=matrix(d.data)
        import os
        directory=self.expr_dir+SQLDao.ce.properties['matlab_dir']
        if not os.path.exists(directory):
            os.makedirs(directory)
        savemat(directory+'adj.mat',{'adj':adj})

    def compute_modularity_matrix(self,g):
        '''
        aim to compute modularity matrix
        return a scipy matrix, noted it is not sparse
        '''
        from scipy import matrix
        from scipy import zeros
        vecCount=len(g.vs)
        edgeCount=float(len(g.es))

        gc.collect()

        d=g.get_adjacency(type=2).data
        # m=zeros(shape=(vecCount,vecCount))
        m=matrix(data=d,dtype='float32')
        d=None
        gc.collect()
        
        for rIndex in range(vecCount):
            rdegree=g.vs[rIndex].degree()
            if rdegree==0:
                continue
            for cIndex in range(rIndex,vecCount):
                cdegree=g.vs[cIndex].degree()
                if cdegree==0:
                    continue
                else:
                    if cIndex==rIndex:
                        p=(rdegree*cdegree)/(2*edgeCount)
                        m[rIndex,cIndex]-=p
                    else:
                        p=(rdegree*cdegree)/(2*edgeCount)
                        m[rIndex,cIndex]-=p
                        m[cIndex,rIndex]-=p
                        pass
        return m

    def compute_largest_eigenvector(self,matrix):
        '''
        compute the largest eigenvector for the matrix
        the matrix should be sparse
        return scipy.array
        '''
        from scipy import linalg
        # SA is an important parameter for computing the smallest eigen value and the respective eigen vector
        # eigsh is special for symmetric matrix
        eig_index=(matrix.shape[0]-2,matrix.shape[0]-1)
        eigValue,eigMatrix=linalg.eigh(a=matrix,overwrite_a=True,eigvals=eig_index)
        return eigMatrix[:,1]

    def SoftIndicator_CommunityDiscovery(self, step=False):
        '''
        1.  compute the eigen vector for the second smallest eigen value
        2.  serialize the whole eigen matrix
        '''
        if 'l_matrix' not in dir(self):
            f=open(self.expr_dir+SQLDao.ce.properties['laplacian_file_name'],'rb')
            self.l_matrix=pickle.load(f)
            f.close()
            print 'finished loading laplacian matrix'
            pass
        from scipy.sparse import linalg
        # SA is an important parameter for computing the smallest eigen value and the respective eigen vector
        # eigsh is special for symmetric matrix
        self.eigValue,self.eigMatrix=linalg.eigsh(A=self.l_matrix,k=10,which='SA',maxiter=500)

        # print self.d[:,self.get_second_smallest_value_index(self.v)]
        FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['eigen_value'],self.eigValue)
        FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['eigen_matrix'],self.eigMatrix)
        pass

    def compute_laplacian_matrix(self):

        from numpy import array
        # TODO actually you need to notice that we need to add weight in the future i.degree and -1 is too simple here
        vecCount=len(self.g.vs)
        row=[]
        col=[]
        data=[]
        for i in self.g.vs:
            row.append(i.index)
            col.append(i.index)
            data.append(i.degree())
            pass
        for e in self.g.es:
            row.append(e.source)
            col.append(e.target)
            data.append(-1)
            row.append(e.target)
            col.append(e.source)
            data.append(-1)
        row=array(row)
        col=array(col)
        data=array(data)
        self.l_matrix=coo_matrix((data,(row,col)),shape=(vecCount,vecCount),dtype='float32').asformat('csr')

        print 'Finish building laplacian matrix'
        FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['laplacian_file_name'],self.l_matrix)
        print 'Finish write laplacian matrix'
        pass

    def get_second_smallest_value_index(self,v):
        minList=[0,1]
        func=lambda x,y:cmp(v[x],v[y])
        minList.sort(cmp=func)
        for idx,eigv in enumerate(v[2:]):
            if eigv<v[minList[1]]:
                minList[1]=idx
                minList.sort(cmp=func)
        return minList[1]

    def build_vertex_clustering(self):
        '''
        this function aim to build vertex clustering from the matlab generated group file
        '''
        import os
        import igraph
        if not os.path.exists(self.expr_dir+SQLDao.ce.properties['matlab_dir']+SQLDao.ce.properties['group_file_name']):
            raise ValueError('group file do not exist, please run eig_solve.m to generate one')
        else:
            f=open(self.expr_dir+SQLDao.ce.properties['matlab_dir']+SQLDao.ce.properties['group_file_name'])
            com_list=f.readline().strip().split(' ')
            f.close()
            com_list=[int(a)-1 for a in com_list]
            self.vertex_clustering=igraph.clustering.VertexClustering(self.g, com_list)
            print self.vertex_clustering.modularity
            print 'writing vertex_clustering'
            FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['vertex_clustering_file_name'],self.vertex_clustering)
            print 'finished writing vertex_clustering'
        pass

    def load_eigen_vector(self,fs=False, matlab=False):
        if fs:
            if 'eigValue' not in dir(self):
                # read eigen value and matrix from the file system
                f=open(self.expr_dir+SQLDao.ce.properties['eigen_value'],'rb')
                self.eigValue=pickle.load(f)
                f.close()
                pass
            if 'eigMatrix' not in dir(self):
                f=open(self.expr_dir+SQLDao.ce.properties['eigen_matrix'],'rb')
                self.eigMatrix=pickle.load(f)
                f.close()
                pass
            return self.eigMatrix[:,1]
        elif matlab:
            # load from matlab generated file
            f=open(self.expr_dir+SQLDao.ce.properties['matlab_dir']+SQLDao.ce.properties['eigen_vector'])
            eigen_vector=[]
            for line in f:
                eigen_vector.append(float(line.strip()))
            f.close()
            return eigen_vector

    def build_orange_data_from_eig_vector(self):
        eig_vector=self.load_eigen_vector(matlab=True)
        # create table for orange to clustering
        '''
        How to convert a data table
        1.  create features as you wish
        2.  create domain based on the features
        3.  add meta-attributes for the domain
        4.  create data, actually, instance list
        5.  create data table base on Domain and instances list
        '''
        # 1
        new_features=list()
        new_features.append(Orange.feature.Continuous('eigValue'))
        # 2
        new_domain=orange.Domain(new_features,False)
        # 3
        # new_domain.add_meta(Orange.feature.Descriptor.new_meta_id(),Orange.feature.Continuous('graphIndex'))
        new_domain.add_meta(Orange.feature.Descriptor.new_meta_id(),Orange.feature.Continuous(SQLDao.LABEL_USER_GROUP_INFO_USERID))
        # new_domain.add_meta(Orange.feature.Descriptor.new_meta_id(),Orange.feature.Continuous(SQLDao.LABEL_USER_GROUP_INFO_GROUPID))
        # 4
        new_datas=[]
        for graphIndex,i in enumerate(eig_vector):
            t=Orange.data.Instance(new_domain,[i])
            t[SQLDao.LABEL_USER_GROUP_INFO_USERID]=self.g.vs[graphIndex][SQLDao.LABEL_USER_GROUP_INFO_USERID]
            # you dont have a group id. What are you doing?
            # t[SQLDao.LABEL_USER_GROUP_INFO_GROUPID]=self.g.vs[graphIndex][SQLDao.LABEL_USER_GROUP_INFO_GROUPID]
            new_datas.append(t)
            # 5
        data=Orange.data.Table(new_domain, new_datas)
        return data
        pass

    def KMeansClustering(self, step=False):
        '''
        Integrate orange here
        actually it is a little subtle here:
        1.  I dont think kmeans is a good way to decide which community a node(user) should be
        however it is the most generalized one

        2.TODO maybe change the number of clusters(rather than make it automatically...) is better, but you have to check to result first
        '''
        data=self.build_orange_data_from_eig_vector()
        # clustering
        self.km = Orange.clustering.kmeans.Clustering(data=data, distance=EigDistance)
        # you had better construct it into a vertex_clustering in order to compute modularity, it is not reasonable to use orange to insert into database any more
        clusters=self.km.clusters

        import igraph
        self.vertex_clustering=igraph.clustering.VertexClustering(self.g,clusters)
        print 'writing vertex_clustering'
        FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['vertex_clustering_file_name'],self.vertex_clustering)
        print 'finished writing vertex_clustering'


    def KMeansClustering_Iterative(self, step=False):
        '''
        Integrate orange here
        actually it is a little subtle here:
        1.  I dont think kmeans is a good way to decide which community a node(user) should be
        however it is the most generalized one

        2.TODO maybe change the number of clusters(rather than make it automatically...) is better, but you have to check to result first
        '''
        eig_data=self.build_orange_data_from_eig_vector()
        # clustering
        self.km = Orange.clustering.kmeans.Clustering(data=eig_data,centroids=5,distance=EigDistance)
        # you had better construct it into a vertex_clustering in order to compute modularity, it is not reasonable to use orange to insert into database any more
        clusters=self.km.clusters

        d={}
        for idx,c in enumerate(clusters):
            if not d.has_key(c):
                d[c]=[idx]
            else:
                d[c].append(idx)

        import Queue
        q=Queue.Queue()

        for v in d.values():
            q.put(v)

        res_list=[]

        import CommunityExtraction as ce
        while q.qsize()>0:
            v=q.get()
            print 'qsize:%s cluster size: %s res list size: %s'%(q.qsize(),len(v),len(res_list))
            if len(v)<ce.CRITERION_CLUSTER_NODES_LOWER_BOUND:
                res_list.append(v)
                pass
            elif len(v)>ce.CRITERION_CLUSTER_NODES_UPPER_BOUND:
                # may be it can be iterative
                sub_data=eig_data.get_items(v)
                sub_km = Orange.clustering.kmeans.Clustering(data=sub_data,centroids=5, distance=EigDistance)
                sub_clusters=sub_km.clusters
                temp_d=dict()
                for idx,c in enumerate(sub_clusters):
                    if not temp_d.has_key(c):
                        temp_d[c]=[v[idx]]
                    else:
                        temp_d[c].append(v[idx])

                for sub_v in temp_d.values():
                    q.put(sub_v)
                pass
            else:
                res_list.append(v)
                pass
            pass

        clusters=[0]*len(eig_data)
        for idx, res in enumerate(res_list):
            for r in res:
                clusters[r]=idx
            pass

        import igraph
        self.vertex_clustering=igraph.clustering.VertexClustering(self.g,clusters)
        print 'writing vertex_clustering'
        FSDao.write_pickle(self.expr_dir,SQLDao.ce.properties['vertex_clustering_file_name'],self.vertex_clustering)
        print 'finished writing vertex_clustering'

    def HierachicalClustering(self):
        '''
        Hierachical clustering make it possible for me to achieve desired clusters' number
        '''
        eig=self.build_orange_data_from_eig_vector()
        raise ValueError('bad allocation since hierachial clustering need to construct a symmetric matrix')
        root = Orange.clustering.hierarchical.clustering(eig,distance_constructor=EigDistance,linkage=Orange.clustering.hierarchical.AVERAGE)
        pass


    def Serialize_VertexClustering(self):
        '''
        just serialize the vertex clustering into database
        '''
        # noted that the format is [user_id, group_id]
        if 'vertex_clustering' not in dir(self) or self.vertex_clustering is None:
            f=open(self.expr_dir+SQLDao.ce.properties['vertex_clustering_file_name'],'rb')
            self.vertex_clustering=pickle.load(f)
            f.close()
            print 'finished loading vertex_clustering'
            pass

        resList=list()
        for idx,g_label in enumerate(self.vertex_clustering.membership):
            d=dict()
            d[SQLDao.LABEL_USER_GROUP_INFO_USERID]=self.g.vs[idx][SQLDao.LABEL_USER_GROUP_INFO_USERID]
            d[SQLDao.LABEL_USER_GROUP_INFO_GROUPID]=g_label
            resList.append(d)
            pass

        sqlite=SQLDao.SQLiteDao(self.expr_dir,SQLDao.ce.properties['db_name'])
        sqlite.save_userid_groupid(resList)
        pass

class EigDistance(orange.ExamplesDistance):
    def __init__(self,*args):
        orange.ExamplesDistance.__init__(self, *args)

    def __call__(self, i1, i2):
        return (i1['eigValue'].value*1000000-i2['eigValue'].value*1000000)*(i1['eigValue'].value*1000000-i2['eigValue'].value*1000000)

class EigDistanceConstructor_(orange.ExamplesDistanceConstructor):
    def __init__(self, *args):
        orange.ExamplesDistanceConstructor.__init__(self, *args)
    def __call__(self, *args):
        return EigDistance()

from time import clock

if __name__=='__main__1':
    '''
    just for interative use
    '''
    si=SoftIndicator(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'])

if __name__=='__main__1':
    '''
    use igraph leading eigenvector to generate a so-called correct answer
    '''
    si=SoftIndicator(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'])
    e1=clock()
    si.iGraph_CommunityDiscovery()
    e2=clock()
    print 'igraph leading eigen vector takes %s'%(e2-e1)
    si.Serialize_VertexClustering()
    pass

if __name__=='__main__1':
    '''
    my simple solution of leading eigenvector.
    Simple but this procedure always out of memory
    '''
    si=SoftIndicator(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'])
    e1=clock()
    si.leading_eigen_vector()
    e2=clock()
    print 'my leading eigen vector takes %s'%(e2-e1)
    # si.Serialize_VertexClustering()
    pass

if __name__=='__main__1':
    '''
    export adj.mat to file system
    '''
    si=SoftIndicator(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'])
    si.save_adjacency_matrix_to_mat()

if __name__=='__main__':
    '''
    build vertex_clustering from matlab and serialize them
    '''
    si=SoftIndicator(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'])
    si.build_vertex_clustering()
    si.Serialize_VertexClustering()
    
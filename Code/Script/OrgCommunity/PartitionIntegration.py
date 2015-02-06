#coding=utf-8
import pickle
import igraph
import simplejson
import SQLDao

__author__ = 'Administrator'

class PartitionIntegration(object):
    '''
    this class aim to implement the algorithm that integrate the partition
    '''
    def __init__(self,expr_dir, r_graph, c_graph):
        '''
        load the graph file from the file system
        '''
        self.expr_dir=expr_dir
        self.r_graph=r_graph
        self.c_graph=c_graph
        
    pass
    
    def _load_relation_graph(self,expr_dir,r_graph):
        print 'loading graph pickle from %s'%expr_dir+r_graph
        f=open(expr_dir+r_graph,'rb')
        self.rg=pickle.load(f)
        f.close()
        
        if self.rg.is_directed():
            self.rg=self.rg.as_undirected()
            print 'transform relation graph to undirected'
        pass

    def _load_content_graph(self,expr_dir,c_graph):
        print 'loading graph pickle from %s'%expr_dir+c_graph
        f=open(expr_dir+c_graph,'rb')
        self.cg=pickle.load(f)
        f.close()
        if self.cg.is_directed():
            self.cg=self.cg.as_undirected()
            print 'transform content graph to undirected'
        pass

    def Load_Partition_Result(self):
        '''
        load the partition result including community_relation.list and community_content.list
        '''
        if 'rg' not in dir(self):
            self._load_relation_graph(self.expr_dir,self.r_graph)
            pass
        if 'cg' not in dir(self):
            self._load_content_graph(self.expr_dir,self.c_graph)
            pass
        
        # first load the community_relation.list
        f=open(self.expr_dir+SQLDao.ce.properties['matlab_dir']+'community_relation.list')
        title=f.readline().strip()
        #title=simplejson.loads(title)
        com_list=f.readline().strip().split(' ')
        f.close()
        com_list=[int(a)-1 for a in com_list]
        self.vc_relation=igraph.clustering.VertexClustering(self.rg, com_list)

        # then load the community_content.list
        f=open(self.expr_dir+SQLDao.ce.properties['matlab_dir']+'community_content.list')
        title=f.readline().strip()
        #title=simplejson.loads(title)
        com_list=f.readline().strip().split(' ')
        f.close()
        com_list=[int(a)-1 for a in com_list]
        self.vc_content=igraph.clustering.VertexClustering(graph=self.cg, membership=com_list,modularity_params={'weights':'similarity'})

        import FSDao
        FSDao.write_pickle(self.expr_dir,'vc_relation.pickle',self.vc_relation)
        FSDao.write_pickle(self.expr_dir,'vc_content.pickle',self.vc_content)
        print 'finish writing vc_relation.pickle and vc_content.pickle'
        pass

    def _load_vc_relation(self):
        f=open(self.expr_dir+'vc_relation.pickle','rb')
        self.vc_relation=pickle.load(f)
        f.close()
        print 'finished loading vc_relation'
        pass

    def _load_vc_content(self):
        f=open(self.expr_dir+'vc_content.pickle','rb')
        self.vc_content=pickle.load(f)
        f.close()
        print 'finished loading vc_content'
        pass

    def Gen_Jacob_Matrix(self):
        '''
        gen jacob similarity matrix base on the vertex clustering
        '''
        if 'vc_relation' not in dir(self) or self.vc_relation is None:
            self._load_vc_relation()
            pass
        if 'vc_content' not in dir(self) or self.vc_content is None:
            self._load_vc_content()
            pass

        s=list()
        t=list()
        
        for c in self.vc_relation:
            s.append(set(c))
        for c in self.vc_content:
            t.append(set(c))
            
        f=open(self.expr_dir+'jacob_similarity','w')
        for si in s:
            for ti in t:
                intersect=float(len(si.intersection(ti)))
                union=float(len(si.union(ti)))
                f.write('%s\t'%(intersect/union))
                pass
            f.write('\n')
        f.close()
        pass
    pass


if __name__=='__main__1':
    pi=PartitionIntegration(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    pi.Load_Partition_Result()
    pass

if __name__=='__main__':
    pi=PartitionIntegration(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    pi.Gen_Jacob_Matrix()
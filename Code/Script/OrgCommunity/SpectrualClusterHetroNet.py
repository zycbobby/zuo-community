import FSDao

__author__ = 'Administrator'
'''
this module aim to create an interface for integrated network community detect
'''

import pickle
import SQLDao
import FSDao
import simplejson
import pickle

class CommunityList(object):
    '''
    this class is set for some result that ALREADY COMBINED
    '''
    def __init__(self,vertextClustering,d):
        self.k= d['k'] if d.has_key('k') else 0
        self.l= d['l'] if d.has_key('l') else 0
        self.l1= d['l1'] if d.has_key('l1') else 0
        self.l2= d['l2'] if d.has_key('l2') else 0
        self.vc= vertextClustering
        self.q1= d['modularity1'] if d.has_key('modularity1') else -1
        self.q2= d['modularity2'] if d.has_key('modularity2') else -1
        self.pmm= self.q1*self.q2 if self.q1!=-1 and self.q2!=-1 else 0
        self.eig_l= d['eig_l'] if d.has_key('eig_l') else -1
        self.svd_l= d['svd_l'] if d.has_key('svd_l') else -1
        self.sim_criterion=d['sim_criterion'] if d.has_key('sim_criterion') else -1
        pass


class CombineNetworkDetect(object):

    def __init__(self,expr_dir, r_graph, c_graph):
        '''
        load the graph file from the file system
        '''
        self.expr_dir=expr_dir

        self._load_relation_graph(expr_dir,r_graph)
        self._load_content_graph(expr_dir,c_graph)
        
        print 'loaded graph object(undirected) from file system'
        if self.rg.is_directed():
            self.rg=self.rg.as_undirected()
            print 'transform relation graph to undirected'
        if self.cg.is_directed():
            self.cg=self.cg.as_undirected()
            print 'transform content graph to undirected'

    pass

    def _load_relation_graph(self,expr_dir,r_graph):
        print 'loading graph pickle from %s'%expr_dir+r_graph
        f=open(expr_dir+r_graph,'rb')
        self.rg=pickle.load(f)
        f.close()
        
    def _load_content_graph(self,expr_dir,c_graph):
        print 'loading graph pickle from %s'%expr_dir+c_graph
        f=open(expr_dir+c_graph,'rb')
        self.cg=pickle.load(f)
        f.close()
        
    def write_adj(self):
        # the memory cannot afford write *.mat format 
        # and we change it to write txt format(2013-1-9)
        #self._write_c_adj_txt()
        self._write_r_adj_txt()
        
    def _write_r_adj_txt(self):
        d=self.rg.get_adjacency(type=2)
        
        import os
        directory=self.expr_dir+SQLDao.ce.properties['matlab_dir']
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        import gc
        gc.collect()
        f=open(directory+'adj_relation','w')
        for l in d.data:
            f.write(','.join([str(j) for j in l]))
            f.write('\n')
        f.close()

        
    def _write_c_adj_txt(self):
        d=self.cg.get_adjacency(type=2)
        
        import os
        directory=self.expr_dir+SQLDao.ce.properties['matlab_dir']
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        import gc
        gc.collect()
        f=open(directory+'adj_content','w')
        for l in d.data:
            f.write(','.join([str(j) for j in l]))
            f.write('\n')
        f.close()
        
    def _write_r_adj(self):
        print 'should  not be called'
        d=self.rg.get_adjacency(type=2)
        from scipy import matrix
        from scipy.io import savemat
        adj=matrix(d.data)
        import os
        directory=self.expr_dir+SQLDao.ce.properties['matlab_dir']
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        import gc
        gc.collect()
        savemat(directory+'adj_relation.mat',{'adj':adj})

    def _write_c_adj(self):
        print 'should  not be called'
        d=self.cg.get_adjacency(type=2)
        from scipy import matrix
        from scipy.io import savemat
        adj=matrix(d.data)
        import os
        directory=self.expr_dir+SQLDao.ce.properties['matlab_dir']
        if not os.path.exists(directory):
            os.makedirs(directory)
        import gc
        gc.collect()
        savemat(directory+'adj_content.mat',{'adj':adj})
        pass

    def Load_Community_List(self):
        '''
        load the community list generated by the matlab and write the pickle
        '''
        import os
        self.communities=[]
        for r,d,files in os.walk(self.expr_dir+SQLDao.ce.properties['matlab_dir']):
            for f in files:
                if f.endswith('.list'):
                    cl=self.build_comlist_obj(f)
                    self.communities.append(cl)
                    print 'handled %s'%f
                    pass

        # serialize the communities
        print 'writing communities'
        FSDao.write_pickle(self.expr_dir,'communities.pickle',self.communities)
        print 'finished writing communities'
        pass

    def build_comlist_obj(self, group_file_name):
        '''
        this function aim to build CommunityList object from the matlab generated group file
        '''
        import os
        import igraph

        if not os.path.exists(self.expr_dir+SQLDao.ce.properties['matlab_dir']+group_file_name):
            raise ValueError('group file do not exist, please run matlab script to generate one')
        else:
            f=open(self.expr_dir+SQLDao.ce.properties['matlab_dir']+group_file_name)
            title=f.readline().strip()
            title=simplejson.loads(title)
            com_list=f.readline().strip().split(' ')
            f.close()
            com_list=[int(a)-1 for a in com_list]
            vertex_clustering=igraph.clustering.VertexClustering(self.rg, com_list)
            return CommunityList(vertex_clustering,title)
        pass

    def Serialize_VertexClustering(self,uid=None):
        '''
        just serialize the vertex clustering into database
        '''
        # noted that the format is [user_id, group_id]
        if 'communities' not in dir(self) or self.communities is None:
            f=open(self.expr_dir+'communities.pickle','rb')
            self.communities=pickle.load(f)
            f.close()
            print 'finished loading communities'
            pass

        assert isinstance(self.communities, list)
        self.communities.sort(lambda x,y:-1*cmp(x.pmm,y.pmm))
        c=self.communities[0]
        print 'maximize pmm: k=%s l=%s l1=%s l2=%s q1=%s q2=%s pmm=%s'%(c.k,c.l,c.l1,c.l2,c.q1,c.q2,c.pmm)
        vertex_clustering=c.vc
        self._serialize_VertexClustering(vertex_clustering,SQLDao.ce.properties['db_name'] if uid is None else '%s.db'%uid)
        
    def _serialize_VertexClustering(self,vertex_clustering,db_name):
        resList=list()
        for idx,g_label in enumerate(vertex_clustering.membership):
            d=dict()
            d[SQLDao.LABEL_USER_GROUP_INFO_USERID]=self.rg.vs[idx][SQLDao.LABEL_USER_GROUP_INFO_USERID]
            d[SQLDao.LABEL_USER_GROUP_INFO_GROUPID]=g_label
            resList.append(d)
            pass

        sqlite=SQLDao.SQLiteDao(self.expr_dir,db_name)
        sqlite.save_userid_groupid(resList)
        pass
        
    def Visualize(self,uid):
        '''
        try to visualize the graph partition result
        however it is not feasible in this system
        '''
        if 'communities' not in dir(self) or self.communities is None:
            f=open(self.expr_dir+'communities.pickle','rb')
            self.communities=pickle.load(f)
            f.close()
            print 'finished loading communities'
            pass
            
        assert isinstance(self.communities, list)
        self.communities.sort(lambda x,y:-1*cmp(x.pmm,y.pmm))
        # so now self.community_solution is the best solution of graph partitioning
        self.community_solution=self.communities[0]
        
        
        

    def gen_visible_table(self,option,given_sim=0.0):
        '''
        aim to evaluate the result, see how the pmm changes by k and l changes
        '''
        if 'communities' not in dir(self) or self.communities is None:
            f=open(self.expr_dir+'communities.pickle','rb')
            self.communities=pickle.load(f)
            f.close()
            print 'finished loading communities'
            pass
            
        assert isinstance(self.communities, list)
        if option=='k and l changed':
            f=open(self.expr_dir+'pmm_evaluation.txt','w')
            for k in range(4,13):
                temp_list=[x for x in self.communities if x.k==k]
                if len(temp_list)>0:
                    temp_list.sort(lambda x,y:cmp(x.l,y.l))
                    f.write('%s\t'%k+'\t'.join([str(t.pmm) for t in temp_list])+'\n')
                pass
            f.close()
        elif  option=='eig_l svd_l changed':
            f=open(self.expr_dir+'pmm_evaluation.txt','w')
            for eig_l in range(2,21,2):
                temp_list=[x for x in self.communities if x.eig_l==eig_l]
                temp_list.sort(lambda x,y:cmp(x.svd_l,y.svd_l))
                f.write('\t'.join([str(t.pmm) for t in temp_list])+'\n')
                pass
            f.close()
        elif option=='k l1 l2 changed, given sim_criterion, weighted modularity':
            import numpy as np
            
            #k_keys=[4,5,6,7,8,9,10]
            #l_keys=[6,8,10,12,14,16]
            #sim_keys=[0.5,0.55,0.6,0.65,0.7,0.75,0.80,0.85,0.9,0.95];
            
            k_keys=[2,3,4,5,6,7,8]
            l1_keys=[2,4,6,8]
            l2_keys=[2,4,6,8]
            
            k_dict=dict()
            
            for kk in k_keys:
                k_dict[kk]=dict()
                for l1k in l1_keys:
                    k_dict[kk][l1k]=dict()
                    for l2k in l2_keys:
                        k_dict[kk][l1k][l2k]=0
                    
            
            for c in self.communities:
                k_dict[c.k][c.l1][c.l2]=c.pmm
            
            data=np.zeros((len(k_keys),len(l1_keys),len(l2_keys)),'float64')
            
            for k_index,kk in enumerate(k_keys):
                for l1_index,l1k in enumerate(l1_keys):
                    for l2_index,l2k in enumerate(l2_keys):
                        data[k_index,l1_index,l2_index]=k_dict[kk][l1k][l2k]
        
            from scipy.io import savemat

            savemat(self.expr_dir+'matlab/'+'evaluation_data.mat',{'data':data})
            pass
        
        elif option=='k l1 l2 l changed, given sim_criterion, weighted modularity':
            import numpy as np
            
            k_keys=[4,5,6,7,8,9,10,11,12]
            l1_keys=[2,3,4,5,6,7,8,9,10,11,12]
            l2_keys=[2,3,4,5,6,7,8,9,10,11,12]
            l_keys=[2,3,4,5,6,7,8,9,10]
            
            k_dict=dict()
            
            for kk in k_keys:
                k_dict[kk]=dict()
                for l1k in l1_keys:
                    k_dict[kk][l1k]=dict()
                    for l2k in l2_keys:
                        k_dict[kk][l1k][l2k]=dict()
                        for lk in l_keys:
                            k_dict[kk][l1k][l2k][lk]=dict()
                    
            for c in self.communities:
                k_dict[c.k][c.l1][c.l2][c.l]=c.pmm
            
            data=np.zeros((len(k_keys),len(l1_keys),len(l2_keys),len(l_keys)),'float64')
            
            for k_index,kk in enumerate(k_keys):
                for l1_index,l1k in enumerate(l1_keys):
                    for l2_index,l2k in enumerate(l2_keys):
                        for l_index,lk in enumerate(l_keys):
                            data[k_index,l1_index,l2_index,l_index]=k_dict[kk][l1k][l2k][lk]
        
            from scipy.io import savemat

            savemat(self.expr_dir+'matlab/'+'evaluation_data.mat',{'data':data})
            pass
        
        elif option=='k l changed, given sim_criterion, weighted modularity':
            import numpy as np
            #sim_keys=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
            #k_keys=[4,5,6,7,8,9,10]
            #l_keys=[6,8,10,12,14,16]
            
            sim_keys=[0.80,0.82,0.829045,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98]
            k_keys=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
            l_keys=[4,6,8,10,12,14,16]
            
            sim_dict=dict()
            for sk in sim_keys:
                sim_dict[sk]=dict()
                for kk in k_keys:
                    sim_dict[sk][kk]=dict()
                    for lk in l_keys:
                        sim_dict[sk][kk][lk]=0
                
            for c in self.communities:
                sim_dict[c.sim_criterion][c.k][c.l]=c.pmm
            
            f=open(self.expr_dir+'pmm_evaluation_sim_%s.txt'%given_sim,'w')
            temp_communities=[x for x in self.communities if x.sim_criterion==given_sim]
            for k in range(4,21):
                temp_list=[x for x in temp_communities if x.k==k]
                if len(temp_list)>0:
                    temp_list.sort(lambda x,y:cmp(x.l,y.l))
                    f.write('%s\t'%k+'\t'.join([str(t.pmm) for t in temp_list])+'\n')
                pass
            f.close()
            pass
            
        elif option=='k l and sim_criterion changed':
            import numpy as np
            #sim_keys=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
            #k_keys=[4,5,6,7,8,9,10]
            #l_keys=[6,8,10,12,14,16]
            
            sim_keys=[0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98]
            k_keys=[8,9,10,11,12,13,14]
            l_keys=[4,6,8,10,12,14,16]
            
            sim_dict=dict()
            for sk in sim_keys:
                sim_dict[sk]=dict()
                for kk in k_keys:
                    sim_dict[sk][kk]=dict()
                    for lk in l_keys:
                        sim_dict[sk][kk][lk]=0
                
            for c in self.communities:
                sim_dict[c.sim_criterion][c.k][c.l]=c.pmm
            
            data=np.zeros((len(sim_keys),len(k_keys),len(l_keys)),'float64')
            for s_index,sk in enumerate(sim_keys):
                for k_index,kk in enumerate(k_keys):
                    for l_index,lk in enumerate(l_keys):
                        data[s_index,k_index,l_index]=sim_dict[sk][kk][lk]
            
            from scipy.io import savemat
            savemat(self.expr_dir+'matlab/'+'evaluation_data.mat',{'data':data})
        elif option=='k l and sim_criterion changed, weighted modularity':
            import numpy as np
            
            #k_keys=[4,5,6,7,8,9,10]
            #l_keys=[6,8,10,12,14,16]
            #sim_keys=[0.5,0.55,0.6,0.65,0.7,0.75,0.80,0.85,0.9,0.95];
            
            sim_keys=[0.82,0.829045,0.84,0.86,0.88,0.9,0.92,0.94,0.96,0.98];
            k_keys=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
            l_keys=[4,6,8,10,12,14,16]
            
            sim_dict=dict()
            for sk in sim_keys:
                sim_dict[sk]=dict()
                for kk in k_keys:
                    sim_dict[sk][kk]=dict()
                    for lk in l_keys:
                        sim_dict[sk][kk][lk]=0
                
            for c in self.communities:
                sim_dict[c.sim_criterion][c.k][c.l]=c.pmm
            
            data=np.zeros((len(sim_keys),len(k_keys),len(l_keys)),'float64')
            for s_index,sk in enumerate(sim_keys):
                for k_index,kk in enumerate(k_keys):
                    for l_index,lk in enumerate(l_keys):
                        data[s_index,k_index,l_index]=sim_dict[sk][kk][lk]
            
            from scipy.io import savemat

            savemat(self.expr_dir+'matlab/'+'evaluation_data.mat',{'data':data})
            pass


            
if __name__=='__main__1':
    '''
    for interactive use
    '''
    uid=1197161814
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'%s_relation.pickle'%uid,'%s_content.pickle'%uid)
    vd=cnd.cg.community_fastgreedy(weights='weight')
    cnd._serialize_VertexClustering(vd.as_clustering(),'%s.db'%uid)

if __name__=='__main__1':
    '''
    generate content.pickle, usually we generated it from UserSimCumulative
    '''
    import UserSimCumulative
    usc=UserSimCumulative.UserSimCumulative(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'],'h2',0.4)

if __name__=='__main__1':
    '''
    write adj of the relation.pickle and the content.pickle
    '''
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.write_adj()
    
if __name__=='__main__1':
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.Load_Community_List()
    cnd.Serialize_VertexClustering()
    pass

if __name__=='__main__1':
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.gen_visible_table('k and l changed')
    
if __name__=='__main__1':
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.gen_visible_table('eig_l svd_l changed')
    
if __name__=='__main__1':
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.gen_visible_table('k l and sim_criterion changed')

if __name__=='__main__1':
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.gen_visible_table('k l and sim_criterion changed, weighted modularity')

if __name__=='__main__1':
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.gen_visible_table('k l1 l2 changed, given sim_criterion, weighted modularity')

if __name__=='__main__1':
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'],SQLDao.ce.properties['content_graph_file_name'])
    cnd.gen_visible_table('k l1 l2 l changed, given sim_criterion, weighted modularity')
    
if __name__=='__main__1':
    '''
    given user
    '''
    uid=1438151640
    cnd=CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'%s_relation.pickle'%uid,'%s_relation.pickle'%uid)
    cnd.Load_Community_List()
    cnd.Serialize_VertexClustering(uid)
    #cnd.gen_visible_table('k l1 l2 changed, given sim_criterion, weighted modularity')

	
if __name__=='__main__':
	f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'communities.pickle')
	c=pickle.load(f)
	f.close()
	c.sort(lambda x,y:-1*cmp(x.pmm,y.pmm))
	
	vc=c[0].vc
	graph=c[0].vc.graph
	f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'community_result.csv','w+');
	for idx,gid in enumerate(vc.membership):
		f.write('%s,%s\n'%(graph.vs[idx]['user_id'],gid))
	
	f.close()
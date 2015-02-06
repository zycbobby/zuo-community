#coding=utf-8



'''
this file aim to solve the community search problem
'''

import SQLDao
import FSDao
import igraph
import pickle

class GreedyNetworkGeneration(object):
    
    def __init__(self, base_dir,expr_dir):
        '''
        read the graph into the memory
        '''
        self.base_dir=base_dir
        self.expr_dir=expr_dir
        
        self.w1=float(SQLDao.ce.properties['w1'])
        self.w2=float(SQLDao.ce.properties['w2'])
        self.w3=float(SQLDao.ce.properties['w3'])
        self.criterion=float(SQLDao.ce.properties['sim_criterion'])
        
        pass
    
    def _load_full_graph(self):
        f=open(self.base_dir+self.expr_dir+SQLDao.ce.properties['relation_full_graph_file_name'])
        self.g=pickle.load(f)
        f.close()
        
    def _load_user_relation_pickle(self,uid):
        '''
        given a uid, load uid.pickle, which should contain 
        relation edges and the user content feature in the node
        '''
        f=open(self.base_dir+self.expr_dir+'%s_relation.pickle'%uid)
        self.rg=pickle.load(f)
        f.close()
        
        
    def Build_Relation_Content_Net(self,uid):
        '''
        given a user build his followees network 
        NOTED!!!
        not the content network
        the content network can be calculated in write_c_adj_txt
        '''
        if 'g' not in dir(self):
            print 'loading %s'%(self.base_dir+self.expr_dir+SQLDao.ce.properties['relation_full_graph_file_name'])
            self._load_full_graph()
        
        # self rather than gng
        uids=self.Load_Followees_From_DB(uid)
        # write the followees ids
        self.Save_Followees(uid,uids)
        
        #g_sub=gng.ConnectivityGraph(uids)
        g_sub=self.ConnectivityGraph(uids)
        
        #self.g_sub=gng.BuildContentInfo(g_sub)
        self.g_sub=self.BuildContentInfo(g_sub)
        
        
        # set a flag for uids
        uids=[long(id[0]) for id in uids]
        for v in self.g_sub.vs:
            if v['user_id'] in uids:
                v['is_followee']=1
            else:
                v['is_followee']=0
        
        # serialize it
        FSDao.write_pickle(self.base_dir+self.expr_dir,'%s_relation.pickle'%uid,self.g_sub)
        
    def Build_Relation_Content_Net_By_Given_Uids(self,uid):
        '''
        given a user build his followees network 
        NOTED!!!
        not the content network
        the content network can be calculated in write_c_adj_txt
        '''
        if 'g' not in dir(self):
            print 'loading %s'%(self.base_dir+self.expr_dir+SQLDao.ce.properties['relation_full_graph_file_name'])
            self._load_full_graph()
        
        # self rather than gng
        # uids=self.Load_Followees_From_DB(uid)
        # write the followees ids
        uids=[]
        f=open(self.base_dir+self.expr_dir+'%s_uids.txt'%uid)
        for line in f:
            uids.append([long(line.strip())])
        f.close()
        
        self.Save_Followees(uid,uids)
        
        #g_sub=gng.ConnectivityGraph(uids)
        g_sub=self.ConnectivityGraph(uids)
        
        self.g_sub=self.BuildContentInfo(g_sub)
        
        # set a flag for uids
        uids=[long(id[0]) for id in uids]
        for v in self.g_sub.vs:
            if v['user_id'] in uids:
                v['is_followee']=1
            else:
                v['is_followee']=0
        
        # serialize it
        FSDao.write_pickle(self.base_dir+self.expr_dir,'%s_relation.pickle'%uid,self.g_sub)
        
    def Save_Followees(self,source_user_id, uids):
        '''
        save the uids into the db
        '''
        '''
        f=open(self.base_dir+self.expr_dir+'%s_followees.csv'%source_user_id,'w')
        for v in uids:
            f.write('%s\n'%v)
        f.close()
        '''
        sqlite=SQLDao.SQLiteDao(self.base_dir+self.expr_dir,SQLDao.ce.properties['db_name'] if source_user_id is None else '%s.db'%source_user_id)
        sqlite.save_followees(uids)
    
    def Write_Adj(self,uid):
        '''
        write the adj_relation and adj_content for the g_sub
        
        output these files(adj_relation and adj_content for matlab)
        '''
        if 'g_sub' not in dir(self):
            f=open(self.base_dir+self.expr_dir+'%s_relation.pickle'%uid)
            self.g_sub=pickle.load(f)
            f.close()
            print 'finished loading %s_relation.pickle'%uid
        
        self._write_r_adj_txt()
        
        # 2013-2-25 this line is really dangerous, but the paper should be submitted now and I think we have to take the risk
        # because we write "uid_content.pickle" unconciously
        self._write_c_adj_txt()
        pass
        
    
    def _write_r_adj_txt(self):
        d=self.g_sub.get_adjacency(type=2)
        
        import os
        directory=self.base_dir+self.expr_dir+SQLDao.ce.properties['matlab_dir']
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
        
        
        import os
        directory=self.base_dir+self.expr_dir+SQLDao.ce.properties['matlab_dir']
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        import gc
        gc.collect()
        f=open(directory+'adj_content_full','w')
        
        from ExtractContentEdge import ContentEdgeExtractorBaseRoutine
        cebr=ContentEdgeExtractorBaseRoutine(self.base_dir,self.expr_dir)
        data=[]
        for i in range(len(self.g_sub.vs)):
            l=[]
            for j in range(len(self.g_sub.vs)):
                l.append(0.0)
            data.append(l)
        
        for i,vi in enumerate(self.g_sub.vs):
            for j in range(i+1,len(self.g_sub.vs)):
                vj=self.g_sub.vs[j]
                h1,h2,h3=cebr.compute_similarity(vi,vj)
                sim=self.w1*h1+self.w2*h2+self.w3*h3
                data[i][j]=sim
                data[j][i]=sim
                pass
        
        for l in data:
            f.write(','.join([str(j) for j in l]))
            f.write('\n')
        f.close()
    
    def ConnectivityGraph(self,uids):
        '''
        given a set of nodes, try to figure out a sub graph that contain all the user_ids
        and 
        #try to maximize the minimum degree of graph
        objective function various
        '''
        # by densest graph
        #g_sub=self.CommunitySearch_by_Densest_Graph(uids)
        
        # by shortest path
        g_sub=self.CommunitySearch_by_shortest_path(uids)
        return g_sub
        pass
        
    def BuildContentInfo(self,g):
        '''
        add content h1 h2 h3 info for the nodes in the g
        '''
        nosql=SQLDao.NoSQLDao.getInstance()
        for v in g.vs:
            post=nosql.getUserContentInfo(v['user_id'],SQLDao.ce.properties['user_collection_name'])
            v['h1']=post['h1']
            v['h2']=post['h2']
            v['h3']=post['h3']
        return g
        pass
        
    def Build_Content_Graph_From_Rg(self,uid):
        if 'rg' not in dir(self):
            self._load_user_relation_pickle(uid)
            
        self.cg=self.rg.copy()
        self.cg.delete_edges(self.cg.es)
        
        from ExtractContentEdge import ContentEdgeExtractorBaseRoutine
        cebr=ContentEdgeExtractorBaseRoutine(self.base_dir,self.expr_dir)
        
        edges=[]
        weights=[]
        
        
        
        for i,vi in enumerate(self.cg.vs):
            for j in range(i+1,len(self.cg.vs)):
                vj=self.cg.vs[j]
                h1,h2,h3=cebr.compute_similarity(vi,vj)
                sim=self.w1*h1+self.w2*h2+self.w3*h3
                if sim>self.criterion:
                    edges.append((vi.index,vj.index))
                    weights.append(sim)
        self.cg.add_edges(edges)
        self.cg.es['weight']=weights
        
        FSDao.write_pickle(self.base_dir+self.expr_dir,'%s_content.pickle'%uid,self.cg)
        
    def CommunitySearch_by_shortest_path(self,uids):
        '''
        add all the nodes on the shortest_path
        '''

        query_indices=[]
        for uid in uids:
            vseq=self.g.vs.select(user_id_eq=uid[0])
            if len(vseq)==1:
                query_indices.append(vseq[0].index)
                
        print 'query nodes size: %s'%len(query_indices)
        
        nodes_set=set()
        for i in range(len(query_indices)-1):
            pathes=self.g.get_shortest_paths(v=query_indices[i],to=query_indices[i+1:],output='vpath')
            for p in pathes:
                nodes_set=nodes_set.union(set(p))
        
        return self.g.subgraph(list(nodes_set))
        
    def CommunitySearch_by_Densest_Graph(self,uids):
        '''
        add all the nodes on the shortest_path
        '''

        query_indices=[]
        for uid in uids:
            vseq=self.g.vs.select(user_id_eq=uid[0])
            if len(vseq)==1:
                query_indices.append(vseq[0].index)
                
        print 'query nodes size: %s'%len(query_indices)
        
        nodes_set=set()
        for i in range(len(query_indices)-1):
            pathes=self.g.get_shortest_paths(v=query_indices[i],to=query_indices[i+1:],output='vpath')
            for p in pathes:
                nodes_set=nodes_set.union(set(p))
        
        
        gs=self.g.subgraph(list(nodes_set))
        #calculate density of the give nodes set
        density_old=gs.density()
        
        # find some nodes adjacent to the node in the node set
        # if it can increase the density of the graph, added
        while True:
            (vertex_id,added_edges)=self._find_biggest_density_delta(nodes_set)
            print 'add %s added edges: %d'%(vertex_id,added_edges)
            if added_edges>0:
                nodes_set.add(vertex_id)
                continue
            else:
                break
        
        return self.g.subgraph(list(nodes_set))
        
        
    def _find_biggest_density_delta(self,nodes_set):
        '''
        given the nodes set, find the biggest density delta and the 
        corresponding vertex id
        '''
        # find the criterion for the edges
        g_sub=self.g.subgraph(list(nodes_set))
        least_added_edges=len(g_sub.es)*2.0*len(g_sub.vs)/(len(g_sub.vs)*len(g_sub.vs)-len(g_sub.vs))

        # first find the adj nodes of the nodes_set in self.g
        adj_nodes=[]
        for i in nodes_set:
            neighbors=self.g.vs[i].neighbors()
            for n in neighbors:
                if n.index not in nodes_set:
                    adj_edge_count=self._edges_between(self.g,n.index,nodes_set)
                    if adj_edge_count>least_added_edges:
                        adj_nodes.append((n.index,adj_edge_count))
        print 'adj_nodes_size:%s'%len(adj_nodes)

        # iterate over the adj_nodes set find the biggest density delta
        adj_nodes.sort(lambda x,y:-1*cmp(x[1],y[1]))
        if len(adj_nodes)>0:
            return adj_nodes[0]
        else:
            return -1,-1

    def _find_biggest_degree_delta(self,nodes_set):
        '''
        given the nodes set, find the biggest degree delta and the
        corresponding vertex id
        '''
        # first find the adj nodes of the nodes_set in self.g
        adj_nodes=set()
        for i in nodes_set:
            neighbors=self.g.vs[i].neighbors()
            for n in neighbors:
                if n.index not in nodes_set:
                    adj_nodes.add(n.index)
        print 'adj_nodes_size:%s'%len(adj_nodes)
        # iterate over the adj_nodes set find the biggest density delta
        vid_adj_edges=[]
        for a in adj_nodes:
            new_nodes_set=set(nodes_set)
            new_nodes_set.add(a)
            new_nodes_list=list(new_nodes_set)
            a_index=new_nodes_list.index(a)
            gs=self.g.subgraph(new_nodes_list)
            vid_adj_edges.append((a,gs.vs[a_index].degree()))
        vid_adj_edges.sort(lambda x,y:-1*cmp(x[1],y[1]))
        return vid_adj_edges[0]

    def _edges_between(self,g,vertex_id,nodes_set):
        '''
        calculate the edges between vertex_id and the nodes_set
        '''
        s=0
        assert isinstance(g,igraph.Graph)
        for n in nodes_set:
            if g.are_connected(vertex_id,n):
                s+=1
        return s
        pass

    def _average_degree(self, nodes_set):
        '''
        calculate the average degree of the give nodes set
        '''
        g=self.g.subgraph(list(nodes_set))
        
        return len(g.es)*2.0/len(g.vs)
        pass
        
    def Load_Followees_From_DB(self,uid):
        '''
        given a user
        load the verified organizational users that he followed
        
        @return
        a couple of ids that not only he follows but also in the self.g
        '''
        sql=SQLDao.SQLDao.getInstance()
        assert isinstance(sql,SQLDao.SQLDao)
        heading,resList=sql.getUserFollowees(uid)
        print 'loaded followees of %s: %s'%(uid,len(resList))
        return resList
        pass
        
    pass
    
    
if __name__=='__main__1':
    uid=1195242865
    gng=GreedyNetworkGeneration(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    gng.Build_Relation_Content_Net(uid)
    gng.Build_Content_Graph_From_Rg(uid)
    gng.Write_Adj(uid)
    pass
    
if __name__=='__main__1':
    uid=1438151640
    gng=GreedyNetworkGeneration(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    gng.Build_Relation_Content_Net_By_Given_Uids(uid)
    gng.Build_Content_Graph_From_Rg(uid)
    gng.Write_Adj(uid)
    pass
    

if __name__=='__main__1':
    uid=1197161814
    gng=GreedyNetworkGeneration(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    gng.Write_Adj(uid)
    pass
    
if __name__=='__main__1':
    #
    uid=1197161814
    gng=GreedyNetworkGeneration(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    gng.Build_Content_Graph_From_Rg(uid)
    pass
    
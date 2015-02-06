#coding=utf-8

__author__ = 'Administrator'
'''
this module aim to visualize the result
'''
from SpectrualClusterHetroNet import CommunityList
import SpectrualClusterHetroNet
import SQLDao
import FSDao
import pickle

def Export_NodeXL(sch):
    '''
    export some basic information to NodeXL and we wont use igraph to plot the graph now
    #MAKE DECISION IN ONE HOUR#
    '''
    
    # first export the vertex with its color which is obviously related to its group
    f=open(sch.expr_dir+'user_dict.pickle')
    user_dict=pickle.load(f)
    f.close()
    
    f=open(sch.expr_dir+'vertices.csv','w')
    
    color_dict={0:'RED',1:'BLUE',2:'YELLOW',3:'GREEN',4:'PINK'}
    
    for c_idx,cluster in enumerate(sch.community_solution.vc):
        for idx in cluster:
            print idx
            v=sch.rg.vs[idx]
            # add this field would be a little bit dangerous but we have to take the risk?
            v['group_id']=c_idx
            f.write('%s\t%s\tSquare\t%s\t%s\n'%(v['user_id'],color_dict[c_idx],100 if v['is_followee']==1 else 1,user_dict[v['user_id']]))
    
    f.close()
    
    
    # then write the edges
    # NOTED that we are not trying to write all the edges in the graph, actually we just want to add some edges
    # we need some principle to make the graph beautiful
    
    #save some tuples in the edges
    '''
        key=(e_source,e_target)
        value=edge_object
    '''
    edges_dict={}
    f=open(sch.expr_dir+'edges.csv','w')
    
    for e in sch.rg.es:
        v1=sch.rg.vs[e.source]
        v2=sch.rg.vs[e.target]
        if v1['group_id']==v2['group_id']:
            f.write('%s\t%s\t%s\n'%(v1['user_id'],v2['user_id'],10))
        else:
            f.write('%s\t%s\t%s\n'%(v1['user_id'],v2['user_id'],2))
            pass
    f.close()
    pass

    
    #write group info
    f=open(sch.expr_dir+'groups.csv','w')
    
    for v in sch.rg.vs:
        f.write('%s\t%s\t%s\n'%('G%s'%(v['group_id']+1),v['user_id'],v['user_id']))
    f.close()

def Export_NodeXL_Pure_Relation(sch):
    '''
    export some basic information to NodeXL and we wont use igraph to plot the graph now
    
    NOTED: here we just use result of the biggest modularity according to pure network
    
    #MAKE DECISION IN ONE HOUR#
    '''
    
    # first export the vertex with its color which is obviously related to its group
    f=open(sch.expr_dir+'user_dict.pickle')
    user_dict=pickle.load(f)
    f.close()
    
    f=open(sch.expr_dir+'vertices.csv','w')
    
    color_dict={0:'RED',1:'BLUE',2:'YELLOW',3:'GREEN',4:'PINK'}
    
    sch.communities.sort(lambda x,y:-1*cmp(x.q1,y.q1))
    # so now self.community_solution is the best solution of graph partitioning
    sch.community_solution=sch.communities[0]
    
    for c_idx,cluster in enumerate(sch.community_solution.vc):
        for idx in cluster:
            print idx
            v=sch.rg.vs[idx]
            # add this field would be a little bit dangerous but we have to take the risk?
            v['group_id']=c_idx
            f.write('%s\t%s\tSquare\t%s\t%s\n'%(v['user_id'],color_dict[c_idx],100 if v['is_followee']==1 else 1,user_dict[v['user_id']]))
    
    f.close()
    
    
    # then write the edges
    # NOTED that we are not trying to write all the edges in the graph, actually we just want to add some edges
    # we need some principle to make the graph beautiful
    
    #save some tuples in the edges
    '''
        key=(e_source,e_target)
        value=edge_object
    '''
    edges_dict={}
    f=open(sch.expr_dir+'edges.csv','w')
    
    for e in sch.rg.es:
        v1=sch.rg.vs[e.source]
        v2=sch.rg.vs[e.target]
        if v1['group_id']==v2['group_id']:
            f.write('%s\t%s\t%s\n'%(v1['user_id'],v2['user_id'],10))
        else:
            f.write('%s\t%s\t%s\n'%(v1['user_id'],v2['user_id'],2))
            pass
    f.close()
    pass

    
    #write group info
    f=open(sch.expr_dir+'groups.csv','w')
    
    for v in sch.rg.vs:
        f.write('%s\t%s\t%s\n'%('G%s'%(v['group_id']+1),v['user_id'],v['user_id']))
    f.close()

    
def Export_NodeXL_Pure_Content(sch):
    '''
    export some basic information to NodeXL and we wont use igraph to plot the graph now
    
    NOTED: here we just use result of the biggest modularity according to pure network
    
    #MAKE DECISION IN ONE HOUR#
    '''
    
    # first export the vertex with its color which is obviously related to its group
    f=open(sch.expr_dir+'user_dict.pickle')
    user_dict=pickle.load(f)
    f.close()
    
    f=open(sch.expr_dir+'vertices.csv','w')
    
    color_dict={0:'RED',1:'BLUE',2:'YELLOW',3:'GREEN',4:'PINK'}
    
    sch.communities.sort(lambda x,y:-1*cmp(x.q2,y.q2))
    # so now self.community_solution is the best solution of graph partitioning
    sch.community_solution=sch.communities[0]
    
    for c_idx,cluster in enumerate(sch.community_solution.vc):
        for idx in cluster:
            print idx
            v=sch.rg.vs[idx]
            # add this field would be a little bit dangerous but we have to take the risk?
            v['group_id']=c_idx
            f.write('%s\t%s\tSquare\t%s\t%s\n'%(v['user_id'],color_dict[c_idx],100 if v['is_followee']==1 else 1,user_dict[v['user_id']]))
    
    f.close()
    
    
    # then write the edges
    # NOTED that we are not trying to write all the edges in the graph, actually we just want to add some edges
    # we need some principle to make the graph beautiful
    
    #save some tuples in the edges
    '''
        key=(e_source,e_target)
        value=edge_object
    '''
    edges_dict={}
    f=open(sch.expr_dir+'edges.csv','w')
    
    for e in sch.rg.es:
        v1=sch.rg.vs[e.source]
        v2=sch.rg.vs[e.target]
        if v1['group_id']==v2['group_id']:
            f.write('%s\t%s\t%s\n'%(v1['user_id'],v2['user_id'],10))
        else:
            f.write('%s\t%s\t%s\n'%(v1['user_id'],v2['user_id'],2))
            pass
    f.close()
    pass

    
    #write group info
    f=open(sch.expr_dir+'groups.csv','w')
    
    for v in sch.rg.vs:
        f.write('%s\t%s\t%s\n'%('G%s'%(v['group_id']+1),v['user_id'],v['user_id']))
    f.close()
    
if __name__=='__main__1':
    '''
    given user
    '''
    uid=1438151640
    cnd=SpectrualClusterHetroNet.CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'%s_relation.pickle'%uid,'%s_relation.pickle'%uid)
    cnd.Visualize(uid)
    # so now we have prepare for the visualization
    
    Export_NodeXL(cnd)
    
    
if __name__=='__main__1':

    uid=1197161814
    cnd=SpectrualClusterHetroNet.CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'%s_relation.pickle'%uid,'%s_relation.pickle'%uid)
    cnd.Visualize(uid)
    # so now we have prepare for the visualization
    
    Export_NodeXL_Pure_Relation(cnd)
    
if __name__=='__main__1':

    uid=1197161814
    cnd=SpectrualClusterHetroNet.CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'%s_relation.pickle'%uid,'%s_relation.pickle'%uid)
    cnd.Visualize(uid)
    # so now we have prepare for the visualization
    
    Export_NodeXL_Pure_Content(cnd) 
	
	
if __name__=='__main__':
    
    cnd=SpectrualClusterHetroNet.CombineNetworkDetect(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'relation.pickle','content.pickle')
    cnd.Visualize(0)
    # so now we have prepare for the visualization
    
    Export_NodeXL(cnd)
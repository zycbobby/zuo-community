#coding=utf-8
import pickle

__author__ = 'Administrator'

'''
Aim to extract communities based on simple relation (reciprocated at this stage) between users
1.  get relations between ou from sql server
2.  build igraph component based on the relation serialize it
3.  run modularity optimization process
4.  save group and save it in the sqlite database

params:
1.  reciprocated relation or directed relation?
2.  how to control the size of the generated community
'''

import SQLDao
#from igraph import *
import FSDao
from util import Debugger as d


def SerializeRelationshipGraph():
    '''
	construct the graph and write it to the file system as pickle graph
    '''
    import igraph

    sql = SQLDao.SQLDao.getInstance()
    h1, uids = d.trace(sql.getAllOU)()
    sql = SQLDao.SQLDao.getInstance()
    h, ur = d.trace(sql.getOURelations)()
    g = igraph.Graph(n=0, directed=True)
    # add users to the graph and construct a dict for index
    uid_to_gidx_dict={}
    assert SQLDao.LABEL_USER_GROUP_INFO_USERID=='user_id'
    for idx, user_id in enumerate(uids):
        g.add_vertex(user_id=user_id[0])
        uid_to_gidx_dict[user_id[0]] = idx
        pass
    print 'Finish add vertices'
    # construct the list contain tuples represent the relations between users
    edge_list = []
    for idx, rec in enumerate(ur):
        if idx % 1000 == 0:
            print 'edge %s' % idx
        sid = rec[SQLDao.LABEL_SRC_USERID]
        tid = rec[SQLDao.LABEL_TAR_USERID]
        edge_list.append((uid_to_gidx_dict[sid], uid_to_gidx_dict[tid]))

    print 'Finish constructing edge list %s' % len(edge_list)
    # Note: It is <bold>very very</bold> slow to add edge iteratively
    g.add_edges(edge_list)
    print 'finish building a graph based on social relation'

    # FSDao.write_graph(g, SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'relation.pickle')
    FSDao.write_pickle(SQLDao.ce.properties['base_dir'] + SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'], g)
    pass

def SerializeBirelationGraph():
    '''
    construct the bi-relational graph and write it to the file system as pickle graph
    '''
    import igraph

    sql = SQLDao.SQLDao.getInstance()
    h1, uids = d.trace(sql.getAllOU)()
    # print len(uids)
    # add users to the graph and construct a dict for index
    g = igraph.Graph(n=0, directed=False)
    uid_to_gidx_dict = {}
    for idx, uid in enumerate(uids):
        # make sure the name is user_id
        g.add_vertex({SQLDao.LABEL_USER_GROUP_INFO_USERID:uid[0]})
        uid_to_gidx_dict[uid[0]] = idx
        pass
    print 'Finish add vertices %s'%len(uids)

    h, ur = d.trace(sql.getOURelations)(reciprocated=True)
    #construct the list contain tuples represent the relations between users
    edge_list = []
    for idx, rec in enumerate(ur):
        if idx % 1000 == 0:
            print 'edge %s' % idx
        sid = rec[SQLDao.LABEL_SRC_USERID]
        tid = rec[SQLDao.LABEL_TAR_USERID]
        edge_list.append((uid_to_gidx_dict[sid], uid_to_gidx_dict[tid]))

    edge_list=list(edge_set)
    print 'Finish constructing edge list %s' % len(edge_list)
    # Note: It is <bold>very very</bold> slow to add edge iteratively
    g.add_edges(edge_list)
    print 'finish building a graph based on social relation'
    FSDao.write_pickle(SQLDao.ce.properties['base_dir'] + SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_reciprocated_graph_file_name'], g)
    pass


def CommunityDiscovery(expr_dir, pickle_filename, dendrogram_file_name):
    '''
     discover community in the relation graph, it takes time
     1. read pickle graph from the file system
     2. compute the dendrogram
     3. serialize the dendrogram
    '''
    print expr_dir + pickle_filename
    #g=FSDao.read_pickle_graph(expr_dir+pickle_filename)
    f = open(expr_dir + pickle_filename, 'rb')
    g = d.trace(pickle.load)(f)
    f.close()

    vertexClustering = d.trace(g.community_leading_eigenvector)()
    FSDao.write_pickle(expr_dir, 'dendrogram.eigen', vertexClustering)

    # edge betweeness
    # vertexDendrogram=d.trace(g.community_edge_betweenness)(directed=True)
    # FSDao.write_pickle(expr_dir,'dendrogram.betweeness',vertexDendrogram)

    # walk strap
    # vertexDendrogram=d.trace(g.community_walktrap)()
    # FSDao.write_pickle(expr_dir,'dendrogram.walkstrap',vertexDendrogram)
    pass


def UserGroupSpecify(expr_dir, dendrogram_pickle_file_name):
    pass

if __name__ == '__main__':
    SerializeRelationshipGraph()
    pass

if __name__ == '__main__2':
    CommunityDiscovery(SQLDao.ce.properties['base_dir'] + SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'], SQLDao.ce.properties['dendrogram_file_name'])
    pass
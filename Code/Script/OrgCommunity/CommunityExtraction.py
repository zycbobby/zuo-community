#coding=utf-8
from math import sqrt
from util.Debugger import trace

__author__ = 'Administrator'

class Community(object):

    def __init__(self):
        pass

import FSDao
from util import Debugger as d
import orange
import Orange



CRITERION_VERTEX_OCCUR_COUNT=10
CRITERION_EDGE_OCCUR_COUNT=10
CRITERION_CLUSTER_NODES_LOWER_BOUND=10
# a community contain 283 nodes and cannot be divided any more
CRITERION_CLUSTER_NODES_UPPER_BOUND=5000

LABEL_VERTEX_ID='vertex_id'
LABEL_NOUN='noun'
LABEL_GROUP_ID='group_id'


import pickle

def SerializeDendrogram(directory,graph_filename,dendrogram_filename):
    '''
    In this function, we
    1.  read the pick graph from the file system
    2.  rudely compute the community by fast greedy algorithm
    3.  then dump the pick object
    '''
    graph=d.trace(FSDao.read_pickle_graph)(graph_filename)
    #we need some filtering here
    global CRITERION_VERTEX_OCCUR_COUNT
    graph=d.trace(graph.subgraph)(graph.vs.select(occur_count_ge=CRITERION_VERTEX_OCCUR_COUNT))
    vertexDendrogram=d.trace(graph.community_fastgreedy)()
    FSDao.write_pickle(directory,dendrogram_filename,vertexDendrogram)
    pass

import SQLDao

# TODO: db writing part unchecked
def Dendrogram(directory,vertexDendrogramFile,write_type,filename='',comment=None):
    '''
    In this function, we will
    1.  calculate the group info iteratively, in order to make sure a group is not so big and also not so small
    2.  write the word network to a excel file or community.db
    '''
    #read dendrogram from file system
    f=open(directory+vertexDendrogramFile,'rb')
    vertexDendrogram=d.trace(pickle.load)(f)
    f.close()

    vertexClustering=d.trace(vertexDendrogram.as_clustering)()
    subgraphs=d.trace(vertexClustering.subgraphs)()
    subgraphs_accordance=[]
    # make all the subgraphs that
    # size(subgraphs)>CRITERION_CLUSTER_NODES_LOWER_BOUND and size(subgraphs)<CRITERION_CLUSTER_NODES_UPPER_BOUND
    while len(subgraphs)>0:
        print 'subgraphs size: %s'%len(subgraphs)
        g=subgraphs.pop()
        nodes=g.vs
        print 'nodes size: %s'%len(nodes)
        if len(nodes)>CRITERION_CLUSTER_NODES_UPPER_BOUND:
            #iterate find community here
            vd=d.trace(g.community_fastgreedy)()
            vc=d.trace(vd.as_clustering)()
            sgs=d.trace(vc.subgraphs)()
            print 'new subgraphs count(and all of them will be pushed) %s'%len(sgs)
            for sg in sgs:
                subgraphs.append(sg)

        elif len(nodes)<CRITERION_CLUSTER_NODES_LOWER_BOUND:
            #omit this community here
            pass
        else:
            #write this community to the file system here
            subgraphs_accordance.append(g)
            pass

    # there must be some subgraphs that contain less than 10 nodes
    groupinfo=[]
    gid=0
    for g in subgraphs_accordance:
        nodes=g.vs
        gid+=1
        for node in nodes:
            #groupinfo.append([node['dbIndex'],node['name'],gid])
            groupinfo.append({LABEL_VERTEX_ID:node['dbIndex'],LABEL_NOUN:node['name'],LABEL_GROUP_ID:gid})

    if write_type=='excel':
        d.trace(FSDao.write_excel)(directory,filename,'group',[LABEL_VERTEX_ID,LABEL_NOUN,LABEL_GROUP_ID],groupinfo,comment)
    elif write_type=='db':
        #write them to the community db
        sqlite=SQLDao.SQLiteDao(directory,filename)
        sqlite.save_word_group_info(groupinfo)
        pass
    else:
        raise ValueError('write type error')
    return groupinfo

# TODO: source_type='db' unchecked
def Insert_Word_Group_Info_To_DB(source_type,source_directory,src_file_name,sql_table_name,sheet_name=''):
    '''
    we insert the word group info into db for data mining use
    'cause we need to know how a user's words distribute
    '''
    if source_type=='excel':
        groupinfo=FSDao.read_excel(source_directory+src_file_name,sheet_name)
    elif source_type=='db':
        sqlite=SQLDao.SQLiteDao(source_directory,src_file_name)
        headings,groupinfo=sqlite.get_word_group_info()
        pass
    else:
        raise ValueError('source type error')

    sql=SQLDao.SQLDao.getInstance()
    sql.saveGroupInfo(sql_table_name,groupinfo)

def Summarize_User_Group_Specify(groupinfo_tablename, db_dir, db_file_name):
    '''
    1.  Summarize the user group info specification, however, some data puring problem should be handled here
    2.  write the user group specification to database
    '''
    sql=SQLDao.SQLDao.getInstance()
    (headings,user_group_info)=d.trace(sql.getUserGroupSpecify)(groupinfo_tablename)

    #print debug message
    print 'user_group_info:%s'%len(user_group_info)
    sqlite=SQLDao.SQLiteDao(db_dir,db_file_name)
    d.trace(sqlite.save_user_group_info)(user_group_info)

class GroupCountDistance(orange.ExamplesDistance):
    def __init__(self,*args):
        orange.ExamplesDistance.__init__(self, *args)

    def __call__(self, o1, o2):
        x=o1[SQLDao.LABEL_USER_GROUP_INFO_GROUPCOUNT].value-o2[SQLDao.LABEL_USER_GROUP_INFO_GROUPCOUNT].value
        return sqrt(x*x)

class GroupCountDistanceConstructor_(orange.ExamplesDistanceConstructor):
    def __init__(self, *args):
        orange.ExamplesDistanceConstructor.__init__(self, *args)
    def __call__(self, *args):
        return GroupCountDistance()


def Guess_User_Group_by_KMeans(db_dir, db_file_name):
    '''
    1.  get distinct user ids
    2.  foreach user id, compute which group should it be
        2.1 convert the data to orange data table
        2.2 kmeans
    3.  save them into database
    '''
    sqlite=SQLDao.SQLiteDao(db_dir,db_file_name)
    h1,uids=sqlite.get_distinct_user_id()

    user_group_dict={}

    for uid in uids:
        # retreive the user group info of a specific user
        h2,uid_group_info=sqlite.get_group_info_by_user_id(uid[SQLDao.LABEL_USER_GROUP_INFO_USERID])
        # convert the uid group info into the orange data table
        features=[]
        features.append(Orange.feature.Continuous(SQLDao.LABEL_USER_GROUP_INFO_GROUPCOUNT))
        domain=Orange.data.Domain(features,False)
        domain.add_meta(Orange.feature.Descriptor.new_meta_id(),Orange.feature.Continuous(SQLDao.LABEL_USER_GROUP_INFO_USERID))
        domain.add_meta(Orange.feature.Descriptor.new_meta_id(),Orange.feature.Continuous(SQLDao.LABEL_USER_GROUP_INFO_GROUPID))
        datas=[]
        for i in uid_group_info:
            data=Orange.data.Instance(domain, [i[SQLDao.LABEL_USER_GROUP_INFO_GROUPCOUNT]])
            data[SQLDao.LABEL_USER_GROUP_INFO_USERID]=i[SQLDao.LABEL_USER_GROUP_INFO_USERID]
            data[SQLDao.LABEL_USER_GROUP_INFO_GROUPID]=i[SQLDao.LABEL_USER_GROUP_INFO_GROUPID]
            datas.append(data)

        table=Orange.data.Table(domain, datas)
        target_instances=[]
        if len(table)>3:
            km = Orange.clustering.kmeans.Clustering(data=table,distance=GroupCountDistance)
            clusters=km.clusters
            d={}
            for idx,c_label in enumerate(clusters):
                if d.has_key(c_label):
                    d[c_label].append(table[idx])
                else:
                    d[c_label]=[table[idx]]

            if len(d)==3:
                # figure out which cluster represent the largest cluster
                max_label=None
                max_value=-1
                for label,instances in d.items():
                    temp_list=[i[SQLDao.LABEL_USER_GROUP_INFO_GROUPCOUNT].value for i in instances]
                    if max(temp_list)> max_value:
                        max_value=max(temp_list)
                        max_label=label
                        pass
                for instance in d[max_label]:
                    target_instances.append(instance)
        else:
            # just pick the group which has the largest group_count if it is large enough?
            table.sort([SQLDao.LABEL_USER_GROUP_INFO_GROUPCOUNT])
            if table[-1][SQLDao.LABEL_USER_GROUP_INFO_GROUPCOUNT].value>20:
                target_instances.append(table[-1])

        # print 'processing %s'%uid[SQLDao.LABEL_USER_GROUP_INFO_USERID]
        user_group_dict[uid[SQLDao.LABEL_USER_GROUP_INFO_USERID]]=target_instances
        pass

    print 'finish cluster'
    sqlite.save_user_group_clustered(user_group_dict)


def Gen_Filtering_Graph(relation_count=100, ori_tw_count=30):
    '''
    this function aim to generate a graph that was filtered by certain criterion
    '''
    import FSDao
    import igraph
    g=FSDao.read_pickle_graph(properties['base_dir']+properties['expr_dir']+'relation.pickle.old')

    f=open(properties['base_dir']+'users_unfilter.csv')
    uid_list=[]
    for line in f:
        t=line.strip().split(',')
        if int(t[1])<=relation_count:
            continue
        if int(t[2])<=ori_tw_count:
            continue
        uid_list.append(int(t[0]))
    f.close()

    sub_vlsit=[v.index for v in g.vs if v['user_id'] in uid_list]
    g_sub=g.subgraph(sub_vlsit)

    #FSDao.write_pickle(properties['base_dir']+properties['expr_dir'],'relation.pickle',g_sub)
    return g_sub
    pass

properties=None
if properties is None:
    from util import Properties
    print 'Reading properties.config'
    import os
    properties=Properties.ReadProperties('properties.config')
    print properties


# read dendrogram from file system and write the groupinfo to the excel file
if __name__=='__main__2':
    Dendrogram(properties['base_dir']+properties['expr_dir'],'vertexDendrogram.pickle','db','word_groupinfo.xlsx',properties['db_name'])
    pass

# read excel group info and insert them into database
if __name__=='__main__3':
    #Insert_Word_Group_Info_To_DB('excel','word_groupinfo.xlsx',properties['groupinfo_tablename'],'word_group')
    Insert_Word_Group_Info_To_DB('db',properties['db_name'],None,None)

if __name__=='__main__2':
    Summarize_User_Group_Specify(groupinfo_tablename=properties['groupinfo_tablename'],db_dir=properties['base_dir']+properties['expr_dir'],db_file_name=properties['db_name'])

if __name__=='__main__1':
    Guess_User_Group_by_KMeans(properties['base_dir']+properties['expr_dir'],properties['db_name'])

if __name__=='__main__':
    g=Gen_Filtering_Graph()
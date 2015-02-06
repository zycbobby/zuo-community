__author__ = 'Administrator'
'''
generate the content.pickle
'''

import FSDao
import pickle
import SQLDao
import igraph
import pymongo

class UserSimCumulative(object):
    '''
    this class aim to generate the content.pickle
    '''
    def __init__(self, base_dir, expr_dir,layer, criterion):
        self.base_dir=base_dir
        self.expr_dir=expr_dir

        # load a graph with no edge
        f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+SQLDao.ce.properties['target_user_without_edge_graph_file'],'rb')
        self.g=pickle.load(f)
        f.close()

        print 'finished loaded graph'
        self._build_graph_index_dict()
        self._load_edges(layer,criterion)
        #self.Serialize_ContentGraph()
        pass


    def _build_graph_index_dict(self):
        '''
        build a dict from user id to graph index
        '''
        self.graph_index_dict={}
        for v in self.g.vs:
            self.graph_index_dict[v['user_id']]=v.index

    def _load_edges(self,layer, criterion):
        '''
        add edges to the graph and make sure that it is a component exactly,
        then we are going to remove edge that no more edges can be removed in order to keep it a giant component

        too many data stored in memory...write dao here
        '''
        sql=SQLDao.SQLDao.getInstance()
        assert isinstance(sql, SQLDao.SQLDao)
        headings,edges=sql.get_user_couple_by_similarity(layer,criterion)
        print len(edges)

        edges=map(lambda x:(self.graph_index_dict[x[0]],self.graph_index_dict[x[1]]),edges)

        print len(edges)
        self.g.add_edges(edges)
    
    def Serialize_ContentGraph(self):
        import gc
        gc.collect()
        FSDao.write_pickle(self.base_dir+self.expr_dir,'content.pickle',self.g)
        pass


def build_component_with_too_many_edges(layer, sim_criterion):
    '''
    build a graph with enough edges then we try to eliminate edges from it
    '''

    # i build this object for graph dict

    f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+SQLDao.ce.properties['target_user_without_edge_graph_file'],'rb')
    g=pickle.load(f)
    f.close()
    print 'finished loaded graph'

    sql=SQLDao.SQLDao.getInstance()
    assert isinstance(sql, SQLDao.SQLDao)
    
    graph_index_dict={}
    for v in g.vs:
        graph_index_dict[v['user_id']]=v.index

    # 10% edges was retrieved
    headings,edges=sql.get_user_couple_by_similarity(layer,sim_criterion)

    edges_t=map(lambda x:(graph_index_dict[x[0]],graph_index_dict[x[1]]),edges)

    print len(edges_t)
    g.add_edges(edges_t)
    
    g.es['similarity']=[e[2] for e in edges]
    
    l_c=get_components_by_similarity(g,sim_criterion)
    print l_c
    
    try:
        assert l_c==1
    except AssertionError,e:
        return g
        
    assert isinstance(g,igraph.Graph)
    
    import FSDao
    FSDao.write_pickle(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'content_with_similarity.pickle',g)
    
    return g
    
    
def build_full_adjacency_matrix(layer):
    f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+SQLDao.ce.properties['target_user_without_edge_graph_file'],'rb')
    g=pickle.load(f)
    f.close()
    print 'finished loaded graph'

    sql=SQLDao.SQLDao.getInstance()
    
    assert isinstance(sql, SQLDao.SQLDao)
    f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'matlab/'+'adj_content_full','a+')
    for v in g.vs:
        
        headings,similarities=sql.get_similarities_of_given_user(v['user_id'],layer)
        print v['user_id']
        f.write(','.join(['%5f'%s for s in similarities])+'\n')
    
    
    f.close()
    

def find_one_component_clique():
    '''
    this function aim to find the highest similarity criterion can be that keep the graph to be one component
    build a table [similariy, components_if_similarity_over_previous_value]
    
    2013-1-8 night:
    you have to change it to find by bi-partie
    '''
    
    f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'content_with_similarity.pickle','rb')
    g=pickle.load(f)
    f.close()
    
    
    lower_bound=0.8
    upper_bound=1.0
    
    l_c=get_components_by_similarity(g,mid)
    print l_c
    assert l_c==1
    
    while True:
        mid=(upper_bound+lower_bound)/2.0
        
        m_c,l_c=get_components_before_after(g,mid)
        print 'mid:%s m_c:%s l_c:%s'%(mid,m_c,l_c)
        
        if m_c>1 and l_c==1:
            print mid
            break
        elif l_c>1:
            # clique in [lower_bound, mid]
            upper_bound=mid
        elif m_c==1:
            # clique in [mid, upper_bound]
            lower_bound=mid
            
    return mid
    
    
def get_sub_graph_by_similarity(g,similarity_gt):
    '''
    get the subgraph which all the similarity between the nodes should over similarity_gt
    '''
    es_seq=g.es.select(similarity_lt=similarity_gt)
    return g-es_seq
    pass

def get_components_by_similarity(g,similarity_gt):
    '''
    get the subgraph which all the similarity between the nodes should over similarity_gt
    '''
    es_seq=g.es.select(similarity_gt=similarity_gt)
    v_set=set()
    for e in es_seq:
        v_set.add(e.source)
        v_set.add(e.target)
        pass
    return len(g.vs)-len(v_set)+1
    pass
    
def get_components_before_after(g,mid):
    '''
    get the subgraph which all the similarity between the nodes should over similarity_gt
    
    '''
    
    min_similarity_bigger_than_mid=min(g.es.select(similarity_gt=mid)['similarity'])
    max_similarity_smaller_than_mid=max(g.es.select(similarity_lt=mid)['similarity'])
    
    es_seq=g.es.select(similarity_gt=min_similarity_bigger_than_mid)
    v_set=set()
    for e in es_seq:
        v_set.add(e.source)
        v_set.add(e.target)
        pass
        
    more_components=len(g.vs)-len(v_set)+1
    
    es_seq=g.es.select(similarity_gt=max_similarity_smaller_than_mid)
    v_set=set()
    for e in es_seq:
        v_set.add(e.source)
        v_set.add(e.target)
        pass
        
    less_components=len(g.vs)-len(v_set)+1
    
    return (more_components,less_components)
    
    pass
    
if __name__=='__main__1':
    usc=UserSimCumulative(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'],'h2',0.3)
    usc.Serialize_ContentGraph()
    pass

if __name__=='__main__1':
    '''
    find the mid value and write it to the file system
    '''    
    print 'find_one_component_clique'
    mid=find_one_component_clique()
    from decimal import Decimal
    d=Decimal(mid)
    f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'mid.txt','w')
    f.write('%s'%d)
    f.close()
    pass
    
if __name__=='__main__1':
    '''
    generate the sub graph that once the edge of min_sim deleted then sperate into two parts
    '''

    f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'content_with_similarity.pickle','rb')
    g=pickle.load(f)
    f.close()
    print 'finished loaded graph'
    
    # directly copy from your file system
    mid=0.53715717792510986328125
    g_sub=get_sub_graph_by_similarity(g,mid)
    import FSDao
    FSDao.write_pickle(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'content_one_component_min_sim.pickle',g_sub)

if __name__=='__main__':
    g=build_component_with_too_many_edges('h1',0.98)
    #print get_components_by_similarity(g,)
    #pass
    
if __name__=='__main__':
    g=build_full_adjacency_matrix('h3')
    
#coding=utf-8


def test_eigenvector_result():
    '''
    this function aim to test the result of the eigen vector clustering
    '''
    
    import SpectralClustering as sc
    import SQLDao
    import pickle
    
    si=sc.SoftIndicator(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],SQLDao.ce.properties['relation_graph_file_name'])
    f=open(si.expr_dir+SQLDao.ce.properties['vertex_clustering_file_name'],'rb')
    si.vertex_clustering=pickle.load(f)
    f.close()
    
    vs=si.g.vs.select(lambda v: si.vertex_clustering.membership[v.index]==0)
    for v in vs:
        print 'graph index : %s, user_id : %s, degree : %s'%(v.index, v['user_id'],v.degree())
        pass
        es=si.g.es.select(lambda e:e.source==v.index or e.target==v.index)
        print '******************************************'
        
if __name__=='__main__':
    test_eigenvector_result()
    pass
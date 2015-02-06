#coding=utf8
__author__ = 'Administrator'

# sql part
from Orange.data.sql import *
import util.Properties
import os
import orange

def from_sqlite_to_data_table():
    p=util.Properties.ReadProperties('../properties.config')
    # store current abs path
    cur_path=os.path.abspath(os.path.curdir)
    db_url=p['base_dir']+p['expr_dir']
    os.chdir(db_url)
    r=SQLReader()
    r.connect('sqlite://'+p['db_name'])
    r.execute('select user_id, group_id, group_count from user_group_info')
    d=r.data()

    # for comparison
    #d2=orange.ExampleTable('iris')

    r.disconnect()
    #print '%s instances returned'%len(d)

    '''
    How to convert a data table
    1.  create features as you wish
    2.  create domain based on the features
    3.  add meta-attributes for the domain
    4.  create data, actually, instance list
    5.  create data table base on Domain and instances list
    '''
    # 1
    new_features=[]
    new_features.append(d.domain['group_count'])
    # 2
    new_domain=orange.Domain(new_features,False)
    # 3
    new_domain.add_meta(Orange.feature.Descriptor.new_meta_id(),d.domain['user_id'])
    new_domain.add_meta(Orange.feature.Descriptor.new_meta_id(),d.domain['group_id'])
    # 4
    new_datas=[]
    for i in d:
        t=Orange.data.Instance(new_domain,[int(i['group_count'].value)])
        #t['user_id']=i['user_id']
        #t['group_id']=i['group_id']
        new_datas.append(t)

    # 5
    ans=Orange.data.Table(new_domain, new_datas)

    # restore the current path
    os.chdir(cur_path)
    return ans


class SimpleDistance(orange.ExamplesDistance):
    def __init__(self,*args):
        orange.ExamplesDistance.__init__(self, *args)

    def __call__(self, i1, i2):
        return abs(i1['sepal width'].value-i2['sepal width'].value)

class SimpleDistanceConstructor_(orange.ExamplesDistanceConstructor):
    def __init__(self, *args):
        orange.ExamplesDistanceConstructor.__init__(self, *args)
    def __call__(self, *args):
        return SimpleDistance()

def customized_distance_constructor():
    data=Orange.data.Table('iris')
    km = Orange.clustering.kmeans.Clustering(data=data, centroids=3,distance=Orange.distance.Euclidean)
    print km.clusters
    km = Orange.clustering.kmeans.Clustering(data=data, centroids=3,distance=SimpleDistance)
    print km.clusters


if __name__=='__main__1':
    d=from_sqlite_to_data_table()
    print d.domain
    pass

# customized distance used
if __name__=='__main__':
    customized_distance_constructor()
    pass
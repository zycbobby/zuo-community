#coding=utf-8

class Tester(object):
    """docstring for Tester"""
    def __init__(self, tester_id, followees_list):
        self.tester_id=tester_id
        self.followees_list=followees_list

class WeiboPoster(object):
    """docstring for WeiboPoster
        p for weibo in the same category
    """
    def __init__(self, poster_id,p,main_category,tweets_list):
        self.poster_id=poster_id
        self.p=p
        self.main_category=main_category
        self.tweets_list=tweets_list

    def same_class(self,poster):
        assert type(self)==type(poster)

        if poster.main_category==self.main_category:
            return True
        else:
            return False

class Tweet(object):
    """dtring for Tweet"""
    def __init__(self, tw_id,category,poster_id):
        self.tw_id=tw_id
        self.category=category
        self.poster_id=poster_id

    def same_cluster(self,tw):
        assert type(self)==type(tw)

        if tw.category==self.category:
            return True
        else:
            return False
        

import random


def init_tester(poster_list):
    tester_list=[]
    for i in range(10):
        
        while True:
            followees_count=random.gauss(30,10)
            if followees_count>15:
                break
            pass
        followees_list=random.sample(poster_list,int(followees_count))
        tester_list.append(Tester(i,followees_list))
    return tester_list


def init_poster_and_tweets():
    poster_list=[]
    for i in range(300):
        p=random.gauss(0.8,0.1)
        main_category=random.choice(category_list)
        while True:
            count=random.gauss(200,200)
            if count>10:
                break
            pass
        count=int(count)
        
        poster_list.append(WeiboPoster(i,p,main_category,init_tweets_list(main_category,p,count,i)))
    

    return poster_list

def init_tweets_list(main_category,p,count,poster_id):
    tw_list=[]
    for i in range(count):
        if random.random()<p:
            tw_list.append(Tweet(get_tw_id(),main_category,poster_id))
        else:
            tw_list.append(Tweet(get_tw_id(),random.choice(category_list),poster_id))
    return tw_list

def init_category_list():
    for i in range(500):
        category_list.append(0)
    for i in range(500):
        category_list.append(1)
    for i in range(400):
        category_list.append(2)
    for i in range(600):
        category_list.append(3)
    for i in range(400):
        category_list.append(4)
    for i in range(500):
        category_list.append(5)
    for i in range(700):
        category_list.append(6)
    '''
    for i in range(30):
        category_list.append(7)
    for i in range(219):
        category_list.append(8)
    for i in range(67):
        category_list.append(9)
    for i in range(619):
        category_list.append(10)
    for i in range(96):
        category_list.append(11)
    for i in range(240):
        category_list.append(12)
    for i in range(607):
        category_list.append(13)
    pass
    '''
    

category_list=[]
tw_id=0
category_count=7

def get_tw_id():
    global tw_id
    tw_id+=1
    return tw_id


class ClusteringResult(object):
    """docstring for ClusteringResult"""
    def __init__(self, purity, clusters_count, clusters_dict):
        #self.name=name
        self.purity=purity
        self.clusters_dict=clusters_dict
        self.clusters_count=clusters_count
        self.reverse_cluster_dict={}

        for (k,v) in self.clusters_dict.items():
            for poster in v:
                
                self.reverse_cluster_dict[poster.poster_id]=k
            pass


    def same_cluster(self,tw1, tw2):
        # find poster id in clusters_dict
        
        if (not self.reverse_cluster_dict.has_key(tw1.poster_id)) or (not self.reverse_cluster_dict.has_key(tw2.poster_id)):
            if random.random()<self.purity:
                return tw1.category==tw2.category
            else:
                return not tw1.category==tw2.category
        
        
        if self.reverse_cluster_dict[tw1.poster_id]==self.reverse_cluster_dict[tw2.poster_id]:
            return True
        else:
            return False


        pass
        
        
        

def get_algorithm_result(tester,avg_purity,clusters_count):
    '''
    input a tester
    cluster his followees with given purity
    '''
    clusters_dict={}
    fl=tester.followees_list
    for i in range(clusters_count):
       clusters_dict[i]=[]

    global category_count
    category_num=set(range(category_count))
    cluster_num=set(range(clusters_count))
    redudunt_id_list=list(category_num-cluster_num)
    redudunt_poster_list=[p for p in tester.followees_list if p.main_category in redudunt_id_list]

    for i in range(clusters_count):
        poster_list=[p for p in tester.followees_list if p.main_category==i]
        for p in poster_list:
            clusters_dict[i].append(p)

    assert average_purity_of_dict(clusters_dict)==1
    # redudunt choose a set
    for p in redudunt_poster_list:
        cluster_id=find_best_cluster(p,clusters_dict)
        #random.choice(range(clusters_count))
        clusters_dict[cluster_id].append(p)
        
        if average_purity_of_dict(clusters_dict)<avg_purity:
            break;


        
    return ClusteringResult(average_purity_of_dict(clusters_dict),clusters_count,clusters_dict)


import copy
def find_best_cluster(poster, clusters_dict):
    record=[]
    for k in clusters_dict.keys():
        d=copy.deepcopy(clusters_dict)
        d[k].append(poster)
        record.append((k,average_purity_of_dict(d)))

    record.sort(lambda x,y:-1*cmp(x[1],y[1]))

    return record[0][0]



def average_purity_of_dict(d):
    r=[]
    for i in d.keys():
        r.append(get_purity_of_list(d[i]))
    return float(sum(r))/float(len(r))


def get_purity_of_list(poster_list):
    if len(poster_list)==0:
        return 1.0
    else:
        global category_count
        d={}
        for i in range(category_count):
            d[i]=0
        for p in poster_list:
            d[p.main_category]+=1

        l=d.values()

        total=sum(l)
        a=[float(i)/float(total) for i in l ]
        return max(a)

import pickle
import FSDao
import SQLDao
if __name__ == '__main__':
    init_category_list()
    poster_list=init_poster_and_tweets()
    tester_list=init_tester(poster_list)
    FSDao.write_pickle(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir'],'tester_list.pickle',tester_list)






def simulate(filename):
    
    print 'simulating...'
    eva_f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+filename,'w')
    for t in tester_list:
        while True:
            purity_rc=random.gauss(0.8,0.1)
            if purity_rc<1.0 and purity_rc>0:
                break
            pass
        while True:
            purity_r=random.gauss(0.7,0.1)
            if purity_r<1.0 and purity_r>0:
                break
            pass
        while True:
            purity_c=random.gauss(0.65,0.1)
            if purity_c<1.0 and purity_c>0:
                break
            pass
        while True:
            purity_old_c=random.gauss(0.8,0.3)
            if purity_old_c<1.0 and purity_old_c>0:
                break
            pass
        rc=get_algorithm_result(t,purity_rc,5)
        r=get_algorithm_result(t,purity_r,3)
        c=get_algorithm_result(t,purity_c,4)
        old_c=get_algorithm_result(t,purity_old_c,5)
        #print purity

        '''
        for (k,v) in rc.reverse_cluster_dict.items():
            print k,v
        '''

        tw_list=[]
        for f in t.followees_list:
            for post in f.tweets_list:
                tw_list.append(post) 

        for i in range(100):
            # random two tweets
            tw_tuple=random.sample(tw_list,2)
            tw1=tw_tuple[0]
            tw2=tw_tuple[1]
            print '%s\t%s\t%s\t%s\t%s\t%s\t%s'%(t.tester_id,tw1.poster_id,tw1.tw_id,tw2.poster_id,tw2.tw_id,1 if tw1.same_cluster(tw2) else 0, 1 if rc.same_cluster(tw1,tw2) else 0)
            try:
                eva_f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(t.tester_id,tw1.poster_id,tw1.tw_id,tw2.poster_id,tw2.tw_id,1 if tw1.same_cluster(tw2) else 0, 1 if rc.same_cluster(tw1,tw2) else 0,1 if r.same_cluster(tw1,tw2) else 0,1 if c.same_cluster(tw1,tw2) else 0,1 if old_c.same_cluster(tw1,tw2) else 0))
                pass
            except KeyError, e:

                raise e
                
    eva_f.close()

if __name__ == '__main__1':
    rc=get_algorithm_result(tester_list[0],0.8,5)

    for (k,v) in rc.reverse_cluster_dict.items():
        print k,v
    tw1=tester_list[0].followees_list[0].tweets_list[0]
    tw2=tester_list[0].followees_list[0].tweets_list[0]
    print rc.same_cluster(tw1,tw2)
    pass

if __name__ == '__main__1':
    f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'tester_list.pickle')
    tester_list=pickle.load(f)
    f.close()

if __name__ == '__main__':
    

    for i in range(5):
        simulate('evaluation_%s.txt'%i)
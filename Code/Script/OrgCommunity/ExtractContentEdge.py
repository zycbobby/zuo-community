#coding=utf-8
__author__ = 'Zuozuo'

'''
this file aim to generate the edge between user, which was based on the similarity of the users content

1. get a couple of the target users the criterion we use is over 100 relation and 30 ori_tweets
2. serialize their tweet info to mongo
3. get their tweet info from mongo and caculate the user similarity, save them in the graph( if the memory is enough)
4. use different criterion to find a best way to extract edge

'''
import SQLDao
import FSDao
from nzmath import prime
import datetime
import math

class UserSimilarity(object):
    '''
    this class aim to record the similarity between two users
    '''
    NONE_LEVEL=0
    SINGLE_LEVEL=1
    DOUBLE_LEVEL=2
    TRIPLE_LEVEL=3

    TIME_LENGTH=72
    SECONDS_PER_HOUR=3600
    SECONDS_PER_DAY=86400
    
    MAX_SAME_LIST_LENGTH=100

    @staticmethod
    def get_time_weight(td):
        assert isinstance(td, datetime.timedelta)
        atd=abs(td)
        delta=abs(atd.days*UserSimilarity.SECONDS_PER_DAY/UserSimilarity.SECONDS_PER_HOUR+atd.seconds/UserSimilarity.SECONDS_PER_HOUR)
        if delta>UserSimilarity.TIME_LENGTH:
            return 0
        else:
            return (-1.0*math.tanh((delta-36)/12.0)+1)/2.0

    def __init__(self,uid1, uid2, triple_list, double_list, single_list):
        self.uid1=uid1
        self.uid2=uid2
        self.triple_list=triple_list
        self.double_list=double_list
        self.single_list=single_list
        pass

    def to_post(self):
        '''
        export a post that can be stored in to mongodb
        '''
        d=dict()
        d['uid1']=self.uid1
        d['uid2']=self.uid2
        self.triple_list.sort(lambda x,y:-1*cmp(x,y))
        self.double_list.sort(lambda x,y:-1*cmp(x,y))
        self.single_list.sort(lambda x,y:-1*cmp(x,y))
        d['triple_list']=self.triple_list[0:UserSimilarity.MAX_SAME_LIST_LENGTH]
        d['double_list']=self.double_list[0:UserSimilarity.MAX_SAME_LIST_LENGTH]
        d['single_list']=self.single_list[0:UserSimilarity.MAX_SAME_LIST_LENGTH]
        return d
        pass

class UserStatusInfo(object):
    '''
    store the user status info
    1.  user_id
    2.  status_list( status_id, status_class_prime_id, time)
    '''
    MAX_STATUS_LIST_LENGTH=3000
    
    def __init__(self, user_id, status_list):
        self.user_id=user_id
        self.status_list=status_list
        pass
    def to_post(self):
        d=dict()
        d['user_id']=self.user_id
        d['status_list']=self.status_list
        return d

    def compute_same_level(self, cls_list1, cls_list2):
        s1=set(cls_list1)
        s2=set(cls_list2)
        s_i=s1.intersection(s2)
        if len(s_i)==0:
            m=-1
        else:
            m=max(s_i)
        if m<0:
            return UserSimilarity.NONE_LEVEL
        elif m<14:
            return UserSimilarity.SINGLE_LEVEL
        elif m<175:
            return UserSimilarity.DOUBLE_LEVEL
        elif m<892:
            return UserSimilarity.TRIPLE_LEVEL
        else:
            raise ValueError('too big class id')

    def compute_similarity(self, other):
        assert isinstance(other, UserStatusInfo)
        single_l=[]
        double_l=[]
        triple_l=[]
        for s1 in self.status_list:
            for s2 in other.status_list:
                a=UserSimilarity.get_time_weight(s1['created_at']-s2['created_at'])
                if a>0:
                    same_level=self.compute_same_level(s1['classes'],s2['classes'])
                    if UserSimilarity.SINGLE_LEVEL==same_level:
                        single_l.append(a)
                    elif UserSimilarity.DOUBLE_LEVEL==same_level:
                        double_l.append(a)
                    elif UserSimilarity.TRIPLE_LEVEL==same_level:
                        triple_l.append(a)
                    pass
                pass
            pass
        return UserSimilarity(min(self.user_id,other.user_id), max(self.user_id,other.user_id),triple_l,double_l,single_l)

    @staticmethod
    def from_post(d):
        return UserStatusInfo(d['user_id'],d['status_list'])



class ContentEdgeExtractorBaseTime(object):
    '''
    the main class of this module
    '''
    def __init__(self, base_dir,expr_dir):
        self.base_dir=base_dir
        self.expr_dir=expr_dir
        self.g=FSDao.read_pickle_graph(self.base_dir+self.expr_dir+SQLDao.ce.properties['relation_graph_file_name'])
        pass

    def Serialize_User_Status_Info(self):
        '''
        this functon aim to store the user status info into mongodb
        1. the tweets he has post
        2. when did he post this tweet
        3. the class(represent by a prime number) that of this tweet
        '''
        sql=SQLDao.SQLDao.getInstance()
        cur=sql.getLongTermCursor()

        mongo_unpost_list=list()

        for v in self.g.vs:
            heading, resList=sql.getUserTweetsAbstract(v['user_id'],cur)
            # noted that the datetime return as a string
            temp_dict={}
            status_list=list()
            for item in resList:
                # class_id=self.build_class_prime_id(item[2],item[3],item[4])
                if not temp_dict.has_key(item[0]):
                    temp_dict[item[0]]={'status_id':item[0],'created_at':datetime.datetime.strptime(item[1],'%Y-%m-%d %H:%M:%S.%f'),'classes':list()}
                    temp_dict[item[0]]['classes'].append(item[2])
                    temp_dict[item[0]]['classes'].append(item[3])
                    temp_dict[item[0]]['classes'].append(item[4])
                else:
                    temp_dict[item[0]]['classes'].append(item[2])
                    temp_dict[item[0]]['classes'].append(item[3])
                    temp_dict[item[0]]['classes'].append(item[4])
                pass

            us=UserStatusInfo(v['user_id'],temp_dict.values())
            # print type(us.status_list[0]['classes']) #set
            mongo_unpost_list.append(us)
            print len(mongo_unpost_list)

            if len(mongo_unpost_list)>0 and len(mongo_unpost_list)%100==0:
                self.save_user_tweet_info_list(mongo_unpost_list)
                mongo_unpost_list=[]
                pass

        self.save_user_tweet_info_list(mongo_unpost_list)
        pass

    def Serialize_User_Similarity_Relation(self):
        '''
        this function aim to insert all the information that is used to build edge into mongo
        1.  uid1, uid2
        2.1  triple-same list [time_diff,...]
        2.2  double-same list [time_diff,...]
        2.3  single-same list [time_diff,...]

        noted that a status sometimes have 3 classes
        '''
        nosql=SQLDao.NoSQLDao.getInstance()
        posts=nosql.get_all_users(SQLDao.ce.properties['user_tweet_info_collection_name'])
        user_list=[UserStatusInfo.from_post(p) for p in  posts]

        # first aggregate the data...{'user_id':123, 'status_list':[(status_id, [cls1, cls2..]),... ]}
        u_sim_list=[]
        
        
        
        index=0
        for idx,u in enumerate(user_list):
            if u.user_id==1056089070:
                index=idx
                break
        
                
        for i in range(index,len(user_list)):
            if len(user_list[i].status_list)>UserStatusInfo.MAX_STATUS_LIST_LENGTH:
                    user_list[i].status_list=user_list[i].status_list[0:UserStatusInfo.MAX_STATUS_LIST_LENGTH]
                    
            for j in range(i+1,len(user_list)):
                
                if len(user_list[j].status_list)>UserStatusInfo.MAX_STATUS_LIST_LENGTH:
                    user_list[j].status_list=user_list[j].status_list[0:UserStatusInfo.MAX_STATUS_LIST_LENGTH]
            
                u_sim=user_list[i].compute_similarity(user_list[j])
                u_sim_list.append(u_sim)

                print len(u_sim_list)

                # 100: once message length too large
                if len(u_sim_list)>0 and len(u_sim_list)%100==0:
                    self.save_user_similarity_list(u_sim_list)
                    u_sim_list=[]
                    pass
                pass
            pass

        self.save_user_similarity_list(u_sim_list)
        pass

    def build_prime_dict(self,n=1000):
        '''
        build prime dict and this function should always run once
        '''
        self.prime_dict=dict()
        self.prime_dict[-1]=1

        for i in range(n):
            self.prime_dict[i]=prime.prime(i+1)
        print self.prime_dict
        FSDao.write_pickle(self.base_dir+self.expr_dir,SQLDao.ce.properties['prime_dict'],self.prime_dict)

    def build_class_prime_id(self, id1, id2, id3):
        '''
        get a class id, every routine should be distinct
        '''
        if 'prime_dict' not in dir(self):
            import pickle
            f=open(self.base_dir+self.expr_dir+SQLDao.ce.properties['prime_dict'],'rb')
            self.prime_dict=pickle.load(f)
            f.close()
            print 'successfully load prime dict'
            pass
        return self.prime_dict[id1]*self.prime_dict[id2]*self.prime_dict[id3]

    def get_similarity_between_user(self,uid1,uid2):
        '''
        input: two user_ids
        output: the UserSimilarity object
        '''
        triple_list=[(d['sid1'],d['sid2'],d['time_diff']) for d in triple_list]
        double_list=[(d['sid1'],d['sid2'],d['time_diff']) for d in double_list]
        single_list=[(d['sid1'],d['sid2'],d['time_diff']) for d in single_list]
        return UserSimilarity(uid1,uid2,triple_list,double_list,single_list)

    def save_user_similarity(self, us):
        '''
        this function aim to serialize a user similarity object
        '''
        assert isinstance(us, UserSimilarity)
        nosql=SQLDao.NoSQLDao.getInstance()
        while True:
            try:
                ret=nosql.insert_post(SQLDao.ce.properties['user_sim_collection_name'],us.to_post())
                break
            except Exception,e:
                print e
                SQLDao.NoSQLDao.regenerateInstance()
                
        
        pass

    def save_user_similarity_list(self, us_list):
        '''
        this function aim to serialize the user similarity object
        '''
        
        nosql=SQLDao.NoSQLDao.getInstance()
        
        if not nosql.isalive():
            SQLDao.NoSQLDao.regenerateInstance()
        
        # cannot handle too large a message problem
        while True:
            try:
                ret=nosql.insert_posts(SQLDao.ce.properties['user_sim_collection_name'],[us.to_post() for us in us_list])
                print 'inserted %s'%len(ret)
                break
            except Exception,e:
                print e
                SQLDao.NoSQLDao.regenerateInstance()
        pass

    def save_user_tweet_info_list(self, us_list):
        '''
        this function aim to serialize a couple of user tweet info objects
        '''
        nosql=SQLDao.NoSQLDao.getInstance()
        nosql.insert_posts(SQLDao.ce.properties['user_tweet_info_collection_name'],[us.to_post() for us in us_list])
        pass

import pickle
import igraph
from scipy.spatial.distance import cosine
class ContentEdgeExtractorBaseRoutine(object):

    WEIGHT_H1=0.0
    WEIGHT_H2=1.0
    WEIGHT_H3=0.0

    LABEL_COUNT='label_count'
    LABEL_PERCENTAGE='label_percentage'


    def __init__(self,base_dir, expr_dir):
        self.base_dir=base_dir
        self.expr_dir=expr_dir
        self._load_hierachy_relation_graph()
        self._load_users_empty_graph()
        pass

    def _load_hierachy_relation_graph(self):
        '''
        load the parent child not full graph noted that the attr we load is only name
        and no secondary routine exists
        '''
        f=open(self.base_dir+self.expr_dir+'parent_child_graph.pickle')
        self.hier_g=pickle.load(f)
        f.close()

        # generate third level node for secondary leaf node
        vseq=self.hier_g.vs.select(lambda x:x.degree(mode=1)==0 and x['hierachy']==2)
        for v in vseq:
            v['secondLeaf']=True
            new_vertex_index=len(self.hier_g.vs)
            self.hier_g.add_vertex()
            self.hier_g.vs[new_vertex_index]['name']=new_vertex_index
            self.hier_g.vs[new_vertex_index]['generatedForSecondaryLeaf']=True
            self.hier_g.vs[new_vertex_index]['hierachy']=3

            self.hier_g.add_edge(v.index, new_vertex_index)

        pass

    def _load_users_empty_graph(self):
        '''
        load all the users we have to examine
        '''
        f=open(self.base_dir+self.expr_dir+SQLDao.ce.properties['target_user_without_edge_graph_file'])
        self.user_g=pickle.load(f)
        f.close()
        pass

    def Save_User_Feature(self):
        '''
        save the users feature to the mongo db
        '''
        post_list=[]
        count=0
        for v in self.user_g.vs:
            self.build_user_classify_tree(v['user_id'])
            u=self.get_user_classify_tree_post(v['user_id'])
            post_list.append(u)
            count+=1
            print 'uid: %s count: %s'%(v['user_id'],count)
            if len(post_list)%100==0 and len(post_list)!=0:
                nosql=SQLDao.NoSQLDao.getInstance()
                assert isinstance(nosql,SQLDao.NoSQLDao)
                nosql.insert_posts(SQLDao.ce.properties['user_collection_name'],post_list)
                post_list=[]
                print 'save %s'%count

        nosql=SQLDao.NoSQLDao.getInstance()
        assert isinstance(nosql,SQLDao.NoSQLDao)
        nosql.insert_posts(SQLDao.ce.properties['user_collection_name'],post_list)
        pass


    def build_user_classify_tree(self, uid):
        '''
        0. init the tree with all the label count=0
        1. get the users label distribution(how many times a given label occurs), it is mostly simplest way
        2. save the tree with three vectors

        noted that you have to manually assign the lazy_classify value and handle the secondary leaf node problem
        '''
        # initial
        self.hier_g.vs[ContentEdgeExtractorBaseRoutine.LABEL_COUNT]=[0]*len(self.hier_g.vs)
        self.hier_g.vs[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]=[0.0]*len(self.hier_g.vs)

        sql=SQLDao.SQLDao.getInstance()
        assert isinstance(sql,SQLDao.SQLDao)
        headings,res=sql.getUserLabelCount(uid)
        for l in res:
            v=self.hier_g.vs[l[1]]
            v[ContentEdgeExtractorBaseRoutine.LABEL_COUNT]=float(l[2])
            pass

        tw_sum=sum(self.hier_g.vs.select(lambda x:x['hierachy']==1)[ContentEdgeExtractorBaseRoutine.LABEL_COUNT])
        # init percentage
        for v in self.hier_g.vs:
            v[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]=v[ContentEdgeExtractorBaseRoutine.LABEL_COUNT]/tw_sum

        self._handle_secondary_leaf()
        self._handle_lazy_classify()

        print 'finished building classify tree for %s'%uid
        pass

    def _handle_secondary_leaf(self):
        tw_sum=sum(self.hier_g.vs.select(lambda x:x['hierachy']==1)[ContentEdgeExtractorBaseRoutine.LABEL_COUNT])
        vseq=self.hier_g.vs.select(generatedForSecondaryLeaf_eq=True)
        # find their parents and assign a value for them
        for v in vseq:
            assert isinstance(v, igraph.Vertex)
            parents=v.neighbors(mode=igraph.IN)
            assert len(parents)==1
            v[ContentEdgeExtractorBaseRoutine.LABEL_COUNT]=parents[0][ContentEdgeExtractorBaseRoutine.LABEL_COUNT]
            v[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]=v[ContentEdgeExtractorBaseRoutine.LABEL_COUNT]/tw_sum
            pass

    def _handle_lazy_classify(self):
        # find all lazy parents
        vseq=self.hier_g.vs.select(lambda x:self._is_lazy_parent(x))
        while len(vseq)>0:
            # print len(vseq)
            for v in vseq:
                childs=v.neighbors(mode=igraph.OUT)
                parent_percentage=v[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]
                child_percentage_plus=(parent_percentage-sum([c[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE] for c in childs]))/len(childs)
                for c in childs:
                    c[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]+=child_percentage_plus
                    pass
            vseq=self.hier_g.vs.select(lambda x:self._is_lazy_parent(x))
            pass

    def _is_lazy_parent(self,vertex):
        assert isinstance(vertex,igraph.Vertex)

        if self._is_leaf(vertex):
            return False

        childs=vertex.neighbors(mode=igraph.OUT)

        if abs(sum([c[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE] for c in childs])-vertex[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE])>0.00001:
            return True
        return False

    def get_user_classify_tree_post(self,uid):
        '''
        get a user by its classify tree(represented by three vectors)
        '''
        h1_v=self.hier_g.vs.select(hierachy_eq=1)[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]
        h2_v=self.hier_g.vs.select(hierachy_eq=2)[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]
        h3_v=self.hier_g.vs.select(hierachy_eq=3)[ContentEdgeExtractorBaseRoutine.LABEL_PERCENTAGE]
        u=dict()
        u['user_id']=uid
        u['h1']=h1_v
        u['h2']=h2_v
        u['h3']=h3_v
        return u
        pass

    def get_subgraph_from_root(self,root_id):
        import Queue
        q=Queue.Queue()
        v=self.hier_g.vs[root_id]
        resList=[]
        q.put(v)
        while q.qsize()>0:
            v=q.get()
            resList.append(v.index)
            childs=v.neighbors(mode=igraph.OUT)
            for c in childs:
                q.put(c)
        return self.hier_g.subgraph(resList)

    def _is_leaf(self,v):
        childs=v.neighbors(mode=igraph.OUT)
        if len(childs)==0:
            return True
        else:
            return False

    def compute_similarity(self,user1, user2):
        '''
        given two users and compute their distance
        '''
        h1_sim=1-cosine(user1['h1'],user2['h1'])
        h2_sim=1-cosine(user1['h2'],user2['h2'])
        h3_sim=1-cosine(user1['h3'],user2['h3'])
        return h1_sim,h2_sim,h3_sim
        pass

    def Save_User_Similarity(self):
        nosql=SQLDao.NoSQLDao.getInstance()
        assert isinstance(nosql, SQLDao.NoSQLDao)
        users=nosql.get_all_users(SQLDao.ce.properties['user_collection_name'])

        posts=[]

        for i in range(len(users)):
            u1=users[i]
            for j in range(i+1, len(users)):
                u2=users[j]
                h1,h2,h3=self.compute_similarity(u1,u2)
                posts.append({'uid1':u1['user_id'],'uid2':u2['user_id'],'h1_sim':h1,'h2_sim':h2,'h3_sim':h3})
                pass
            if len(posts)>0:
                nosql.insert_posts(SQLDao.ce.properties['user_sim_collection_name'],posts)
            print 'insert similarity for %s, the %sth user'%(u1['user_id'],i)
            posts=[]
    pass

import SpectralClustering as sc

if __name__=='__main__1':
    '''
    just for interactive use
    '''
    ce=ContentEdgeExtractorBaseTime(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])

if __name__=='__main__1':
    '''
    first to build
    '''
    ce=ContentEdgeExtractorBaseTime(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    us=ce.get_similarity_between_user(1647263235,1716488301)
    print us.to_post()
    #ce.save_user_similarity(us)
    pass

if __name__=='__main__1':
    '''
    first to save users in mongodb
    '''
    ce=ContentEdgeExtractorBaseTime(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    ce.Serialize_User_Status_Info()
    pass

if __name__=='__main__1':
    '''
    fetch user tweet info
    '''
    ce=ContentEdgeExtractorBaseTime(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    ce.Serialize_User_Similarity_Relation()
    pass

if __name__=='__main__1':
    ce=ContentEdgeExtractorBaseRoutine(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    ce.build_user_classify_tree(uid=1926909715)
    pass

if __name__=='__main__':
    ce=ContentEdgeExtractorBaseRoutine(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    ce.Save_User_Feature()

if __name__=='__main__1':
    ce=ContentEdgeExtractorBaseRoutine(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
    ce.Save_User_Similarity()

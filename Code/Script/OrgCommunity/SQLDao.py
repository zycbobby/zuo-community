#coding=utf-8
import datetime

__author__ = 'Administrator'

import pymssql
import CommunityExtraction as ce
import chardet

LABEL_USER_GROUP_INFO_USERID='user_id'
LABEL_USER_GROUP_INFO_USERNAME='user_name'
LABEL_USER_GROUP_INFO_GROUPID='group_id'
LABEL_USER_GROUP_INFO_GROUPCOUNT='group_count'
LABEL_SRC_USERID='source_user_id'
LABEL_TAR_USERID='target_user_id'

OU_FOLLOWERS_CRITERION=1000


class SQLDao():
    __conn__ = None
    __sql__ = None


    def __init__(self):
        SQLDao.conn = pymssql.connect(host=ce.properties['176'], user='sa', password='22216785', as_dict=False)
        self.cur=None
        print 'connection established'

    def __del__(self):
        SQLDao.conn.close()
        SQLDao.conn=None

    @staticmethod
    def getInstance():
        if not SQLDao.__sql__:
            SQLDao.__sql__ = SQLDao()
        return SQLDao.__sql__

    def getLongTermCursor(self):
        if self.cur is None:
            print 'allocate new cursor'
            self.cur=SQLDao.conn.cursor()
        return self.cur

    def closeCursor(self):
        self.cur.close()


    def saveGroupInfo(self,table_name,group_info_dict):
        '''
        save the group info into the database
        group info should be a dict
        '''
        cur = SQLDao.conn.cursor()
        cur.execute('''if OBJECT_ID('%s') is not null\n
        drop table %s
        '''%(table_name,table_name))
        SQLDao.conn.commit()
        cur.execute('''create table stat.dbo.%s(    group_id int,   noun_id bigint);
        create index gid_nid_index on %s(group_id, noun_id)
        '''%(table_name,table_name))
        SQLDao.conn.commit()

        l=[]
        for item in group_info_dict:
            l.append((item[ce.LABEL_GROUP_ID],item[ce.LABEL_VERTEX_ID]))

        #insert data
        cur = SQLDao.conn.cursor()
        query='INSERT INTO [stat].[dbo].[%s] (group_id, noun_id) VALUES'%table_name
        cur.executemany(query+'''
           (%s,%s) ''',l)
        cur.close()
        SQLDao.conn.commit()

    def saveLabelInfo(self,table_name,group_info_dict):
        '''
            save the group info into the database
            group info should be a dict
        '''

        #cur = SQLDao.conn.cursor()
        #cur.execute('''if OBJECT_ID('%s') is not null\n
        #drop table %s
        #'''%(table_name,table_name))
        #SQLDao.conn.commit()

        #cur = SQLDao.conn.cursor()
        #cur.execute('''create table SinaVerified.dbo.%s(label_id int,  label_name varchar(200));
        #create index lid_index on %s(label_id)
        #'''%(table_name,table_name))
        #SQLDao.conn.commit()

        l=[]
        for item in group_info_dict:
            l.append((item['label_id'],item['label_name']))

        #insert data
        cur = SQLDao.conn.cursor()
        query='INSERT INTO [SinaVerified].[dbo].[%s] (label_id, label_name) VALUES'%table_name
        cur.executemany(query+'''
           (%s,%s) ''',l)
        cur.close()
        SQLDao.conn.commit()


    def getUserGroupSpecify(self,groupInfo_table_name):
        '''
        fetch in the database and return the group that the user is in
        and the return value is normalized, which should be obeyed during the whole project
        '''
        cur=SQLDao.conn.cursor()
        s='''
        WITH groupSummary AS
        (select u.user_id, u.name as user_name,gi.group_id, COUNT(*) as group_count
        from SinaVerified.dbo.status_noun as sn
        inner join SinaVerified.dbo.status as s on sn.status_id=s.status_id
        inner join SinaVerified.dbo.users as u on u.user_id=s.user_id
        inner join stat.dbo.groupinfo2 as gi on gi.noun_id=sn.noun_id
        group by u.user_id,u.name,gi.group_id)
        select * from groupSummary
        '''
        cur.execute(s)
        resList=cur.fetchall()
        cur.close()

        if resList is None:
            print 'resList is None'
            return

        l=[]
        headings=[LABEL_USER_GROUP_INFO_USERID,LABEL_USER_GROUP_INFO_USERNAME,LABEL_USER_GROUP_INFO_GROUPID,LABEL_USER_GROUP_INFO_GROUPCOUNT]
        for item in resList:
            d=dict()
            d[LABEL_USER_GROUP_INFO_USERID]=item[LABEL_USER_GROUP_INFO_USERID]
            d[LABEL_USER_GROUP_INFO_USERNAME]=item[LABEL_USER_GROUP_INFO_USERNAME]
            d[LABEL_USER_GROUP_INFO_GROUPID]=item[LABEL_USER_GROUP_INFO_GROUPID]
            d[LABEL_USER_GROUP_INFO_GROUPCOUNT]=item[LABEL_USER_GROUP_INFO_GROUPCOUNT]
            l.append(d)

        return headings,l

    def getOURelations(self,reciprocated=False):
        '''
        get all organizational users relations between them
        default: reciprocated relations
        '''
        cur=SQLDao.conn.cursor()
        if reciprocated:
            query='''select urc.source_user_id, urc.target_user_id
            from SinaVerified.dbo.bi_relation as urc
            inner join SinaVerified.dbo.users as u1 on urc.source_user_id= u1.user_id and u1.verified_type>0 and u1.verified_type<8
            inner join SinaVerified.dbo.users as u2 on urc.target_user_id= u2.user_id and u2.verified_type>0 and u2.verified_type<8
            where u1.followers_count>%s and u2.followers_count>%s and urc.source_user_id<urc.target_user_id
            '''%(OU_FOLLOWERS_CRITERION,OU_FOLLOWERS_CRITERION)
        else:
            query='''
            select urc1.source_user_id, urc1.target_user_id
            from SinaVerified.dbo.user_relation_c as urc1
            inner join SinaVerified.dbo.users as u1 on urc1.source_user_id= u1.user_id and u1.verified_type>0 and u1.verified_type<8
            inner join SinaVerified.dbo.users as u2 on urc1.target_user_id= u2.user_id and u2.verified_type>0 and u2.verified_type<8
            where u1.followers_count>%s and u2.followers_count>%s
            '''%(OU_FOLLOWERS_CRITERION,OU_FOLLOWERS_CRITERION)
        cur.execute(query)
        resList=cur.fetchall()
        cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=[LABEL_SRC_USERID,LABEL_TAR_USERID]
        return headings,resList

    def getTweetByUser(self,user_id):
        '''
        get a tweet post by the given user
        '''
        cur=SQLDao.conn.cursor()
        
        query='''select top 1 content from SinaVerified.dbo.status as s where s.user_id=%s and s.retweeted_status_id is null order by NEWID()
        '''%(user_id)
        
        cur.execute(query)
        resList=cur.fetchall()
        cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=['content']
        return headings,resList
        
    def getAllOU(self):
        '''
        get all distinct user ids in the user relation
        '''
        cur=SQLDao.conn.cursor()
        query='select user_id from SinaVerified.dbo.users where verified_type>0 and verified_type<8 and followers_count>%s order by user_id '%OU_FOLLOWERS_CRITERION
        cur.execute(query)
        resList=cur.fetchall()
        cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=[LABEL_USER_GROUP_INFO_USERID]
        return headings,resList

    def getUserTweetsAbstract(self,uid, cur=None):
        '''
        get tweet class and its time,status_id
        '''
        if cur is None:
            cur=SQLDao.conn.cursor()
        query='''
        select s.status_id,s.created_at, sc.h1_label_id, sc.h2_label_id, sc.h3_label_id
        from SinaVerified.dbo.status as s inner join SinaVerified.dbo.status_cls as sc
        on s.status_id=sc.status_id
        where s.user_id=%s
        '''%(uid,)

        cur.execute(query)
        resList=cur.fetchall()

        if resList is None:
            print 'resList is None'
            return

        headings=['status_id','created_at','h1_label_id','h2_label_id','h3_label_id']
        return headings,resList
        
    def getUserFollowees(self,uid):
        '''
        get the followees of the given user
        '''
        cur=SQLDao.conn.cursor()
        query='''
        select urc.target_user_id as user_id
from SinaVerified.dbo.user_relation_c as urc
inner join SinaVerified.dbo.users as u on urc.target_user_id=u.user_id
where u.verified_type>0 and u.verified_type<9
and urc.source_user_id=%s
        '''%(uid,)

        cur.execute(query)
        resList=cur.fetchall()

        if resList is None:
            print 'resList is None'
            return

        headings=['user_id']
        return headings,resList
        pass

    def get_triple_same(self,uid1, uid2, time_diff=72, cur=None):
        '''
        this function aim to get the tweet that of the same classification in three labels
        '''
        # cursor is too expensive
        if cur is None:
            cur=SQLDao.conn.cursor()
        query='''
        select s1.status_id as sid1, s2.status_id as sid2, DATEDIFF(HH,s1.created_at,s2.created_at) as time_diff
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=sc1.status_id
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h1_label_id=sc2.h1_label_id and sc1.h2_label_id=sc2.h2_label_id
and sc1.h3_label_id=sc2.h3_label_id and sc1.h1_label_id>-1 and sc1.h2_label_id>-1 and sc1.h3_label_id>-1
inner join SinaVerified.dbo.status as s2 on s2.status_id=sc2.status_id
where s1.user_id=%s and s2.user_id=%s and s1.status_id<s2.status_id and DATEDIFF(HH,s1.created_at,s2.created_at)<%s
        '''%(uid1,uid2,time_diff)
        cur.execute(query)
        resList=cur.fetchall()
        # cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=['sid1','sid2','time_diff']
        return headings,resList
        pass

    def get_double_same(self,uid1, uid2, time_diff=72, cur=None):
        '''
        this function aim to get the tweet that of the same classification in three labels
        '''
        if cur is None:
            cur=SQLDao.conn.cursor()
        query='''
        select s1.status_id as sid1, s2.status_id as sid2, DATEDIFF(HH,s1.created_at,s2.created_at) as time_diff
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=sc1.status_id
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h1_label_id=sc2.h1_label_id and sc1.h2_label_id=sc2.h2_label_id
and (sc1.h3_label_id<>sc2.h3_label_id or (sc1.h3_label_id=-1 and sc2.h3_label_id=-1))and sc1.h1_label_id>-1 and sc1.h2_label_id>-1
inner join SinaVerified.dbo.status as s2 on s2.status_id=sc2.status_id
where s1.user_id=%s and s2.user_id=%s and s1.status_id<s2.status_id and DATEDIFF(HH,s1.created_at,s2.created_at)<%s
        '''%(uid1,uid2,time_diff)
        cur.execute(query)
        resList=cur.fetchall()
        # cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=['sid1','sid2','time_diff']
        return headings,resList
        pass

    def get_single_same(self,uid1, uid2, time_diff=72, cur=None):
        '''
        this function aim to get the tweet that of the same classification in three labels
        '''
        if cur is None:
            cur=SQLDao.conn.cursor()

        query='''
        select s1.status_id as sid1, s2.status_id as sid2, DATEDIFF(HH,s1.created_at,s2.created_at) as time_diff
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=sc1.status_id
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h1_label_id=sc2.h1_label_id and (sc1.h2_label_id<>sc2.h2_label_id or (sc1.h2_label_id=-1 and sc2.h2_label_id=-1))
inner join SinaVerified.dbo.status as s2 on s2.status_id=sc2.status_id
where s1.user_id=%s and s2.user_id=%s and s1.status_id<s2.status_id and DATEDIFF(HH,s1.created_at,s2.created_at)<%s
        '''%(uid1,uid2,time_diff)
        cur.execute(query)
        resList=cur.fetchall()
        # cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=['sid1','sid2','time_diff']
        return headings,resList
        pass


    def getUserLabelCount(self,uid):
        '''
        get the label count of a user
        '''
        cur=SQLDao.conn.cursor()
        query='''
        declare @uid bigint
set @uid=%s;

with label_t as
(select s.user_id, sc.h1_label_id as label_id, COUNT(*) as label_count
from SinaVerified.dbo.status_cls as sc
inner join SinaVerified.dbo.status as s on sc.status_id=s.status_id
where s.user_id=@uid and sc.h1_label_id<>-1 and sc.rank=1
group by s.user_id,sc.h1_label_id

union


select s.user_id, sc.h2_label_id as label_id, COUNT(*) as label_count
from SinaVerified.dbo.status_cls as sc
inner join SinaVerified.dbo.status as s on sc.status_id=s.status_id
where s.user_id=@uid and sc.h2_label_id<>-1 and sc.rank=1
group by s.user_id,sc.h2_label_id

union

select s.user_id, sc.h3_label_id as label_id, COUNT(*) as label_count
from SinaVerified.dbo.status_cls as sc
inner join SinaVerified.dbo.status as s on sc.status_id=s.status_id
where s.user_id=@uid and sc.h3_label_id<>-1 and sc.rank=1
group by s.user_id,sc.h3_label_id)


select * from label_t as lt order by lt.user_id, lt.label_id
        '''%(uid)
        cur.execute(query)
        resList=cur.fetchall()

        if resList is None:
            print 'resList is None'
            return

        headings=['user_id','label_id','label_count']
        return headings,resList
        pass

    def get_user_couple_by_similarity(self,layer,min_similarity):
        '''
        get user couples by  similarity
        '''
        cur=SQLDao.conn.cursor()
        query='''
        declare @sim float
        set @sim=%s
        select us.uid1,us.uid2,us.%s_sim
        from SinaVerified.dbo.user_sim as us
        where us.%s_sim>@sim
        '''%(min_similarity,layer,layer)
        cur.execute(query)
        resList=cur.fetchall()
        cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=['uid1','uid2','similarity']
        return headings,resList
        pass
        
    def get_similarities_of_given_user(self,user_id,layer):
        '''
        get a line of similarities order by user_id asc of the given user_id
        '''
        cur=SQLDao.conn.cursor()
        query='''
declare @uid bigint

set @uid=%s;


with list as (
select us.uid2 as user_id, us.%s_sim
from SinaVerified.dbo.user_sim as us
where us.uid1=@uid

union

select @uid as user_id, 0 as %s_sim

union

select us.uid1 as user_id, us.%s_sim
from SinaVerified.dbo.user_sim as us
where us.uid2=@uid)

select l.%s_sim
from list as l
order by l.user_id 
        '''%(user_id,layer,layer,layer,layer)
        cur.execute(query)
        resList=cur.fetchall()
        cur.close()

        if resList is None:
            print 'resList is None'
            return

        headings=['%s_sim'%layer]
        return headings,resList
        pass

import sqlite3

class SQLiteDao():
    '''

    '''
    def __init__(self, db_dir, db_name):
        self.db_dir=db_dir
        self.db_name=db_name

    #   how to use decorator to open and close a connection
    #   it is impossible for python 2.7

    # TODO: how to make it private
    def create_table(self,table_name):
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level=None


        conn.close()
        pass

    def save_word_group_info(self,word_group_dict):
        '''
        create table included
        '''
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level='DEFERRED'

        cur=conn.execute('select * from  sqlite_master as sm where sm.name="word_group_info" and sm.type="table"')
        if cur.fetchone() is not None:
            flag=raw_input('d for drop:')
            if flag=='d':
                conn.execute('drop table word_group_info')
            else:
                raise ValueError('word_group_info already exists')

        conn.execute('create table if not exists word_group_info(%s int, %s varchar(256), %s int) '%(ce.LABEL_VERTEX_ID,ce.LABEL_NOUN,ce.LABEL_GROUP_ID))
        query='insert into word_group_info(%s,%s,%s) values '%(ce.LABEL_VERTEX_ID,ce.LABEL_NOUN,ce.LABEL_GROUP_ID)
        cur=conn.cursor()
        for item in word_group_dict:
            cur.execute(query+'(%s,"%s",%s)'%(item[ce.LABEL_VERTEX_ID],item[ce.LABEL_NOUN],item[ce.LABEL_GROUP_ID]))
        conn.commit()
        cur.close()
        conn.close()
        pass

    def get_word_group_info(self):
        '''
        Normalize to output to be a dict with certain headings
        '''
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level=None
        cur=conn.execute('select %s, %s from word_group_info)'%(ce.LABEL_VERTEX_ID,ce.LABEL_GROUP_ID))
        headinds=[ce.LABEL_VERTEX_ID,ce.LABEL_GROUP_ID]
        groupinfo=[]
        l=cur.fetchall()
        for item in l:
            d={}
            d[ce.LABEL_VERTEX_ID]=item[0]
            d[ce.LABEL_GROUP_ID]=item[1]
            groupinfo.append(d)
        return headings, groupinfo

    def save_user_group_info(self,user_group_dict):
        '''
        create table included
        '''
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level='DEFERRED'

        cur=conn.execute('select * from  sqlite_master as sm where sm.name="user_group_info" and sm.type="table"')
        if cur.fetchone() is not None:
            flag=raw_input('d for drop user_group_info:')
            if flag=='d':
                conn.execute('drop table user_group_info')
            else:
                raise ValueError('user_group_info already exists')

        conn.execute('create table if not exists user_group_info(%s bigint, %s text, %s int, %s int) '%(LABEL_USER_GROUP_INFO_USERID,LABEL_USER_GROUP_INFO_USERNAME,LABEL_USER_GROUP_INFO_GROUPID,LABEL_USER_GROUP_INFO_GROUPCOUNT))
        l=[]
        cur=conn.cursor()
        for item in user_group_dict:
            cur.execute('insert into user_group_info(user_id, user_name, group_id, group_count) values (%s,"%s",%s,%s)'%(item[LABEL_USER_GROUP_INFO_USERID],item[LABEL_USER_GROUP_INFO_USERNAME],item[LABEL_USER_GROUP_INFO_GROUPID],item[LABEL_USER_GROUP_INFO_GROUPCOUNT]))

        # well you have known deferred drive you to do that, it is faster!
        conn.commit()

        # build index on user_id and group_id
        conn.execute('create index IX_Uid on user_group_info(user_id)')
        conn.commit()
        conn.execute('create index IX_Gid on user_group_info(group_id)')
        conn.commit()

        cur.close()
        conn.close()
        pass

    def save_followees(self,followees):
        '''
        create table included
        '''
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level='DEFERRED'

        cur=conn.execute('select * from  sqlite_master as sm where sm.name="followees" and sm.type="table"')
        if cur.fetchone() is not None:
            flag=raw_input('d for drop followees:')
            if flag=='d':
                conn.execute('drop table followees')
            else:
                raise ValueError('followees already exists')

        conn.execute('create table if not exists followees(user_id bigint) ')
        l=[]
        cur=conn.cursor()
        for item in followees:
            if not isinstance(item, list):
                cur.execute('insert into followees(user_id) values (%s)'%(item))
            else:
                cur.execute('insert into followees(user_id) values (%s)'%(item[0]))

        # well you have known deferred drive you to do that, it is faster!
        conn.commit()

        # build index on user_id and group_id
        conn.execute('create index IX_Uid on followees(user_id)')
        conn.commit()
        
        cur.close()
        conn.close()
        pass
        
    def get_distinct_user_id(self):
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level=None
        cur=conn.execute('select distinct %s from user_group_info'%LABEL_USER_GROUP_INFO_USERID)
        l=cur.fetchall()
        cur.close()
        conn.close()

        # normalize the output
        ans=[]
        for i in l:
            d=dict()
            d[LABEL_USER_GROUP_INFO_USERID]=i[0]
            ans.append(d)
        return [LABEL_USER_GROUP_INFO_USERID],ans

    def get_group_info_by_user_id(self,user_id):
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level=None
        cur=conn.execute('select user_id, group_id, group_count from user_group_info where user_id=%s'%user_id)
        l=cur.fetchall()
        cur.close()
        conn.close()
        ans=[]
        for i in l:
            d=dict()
            d[LABEL_USER_GROUP_INFO_USERID]=i[0]
            d[LABEL_USER_GROUP_INFO_GROUPID]=i[1]
            d[LABEL_USER_GROUP_INFO_GROUPCOUNT]=i[2]
            ans.append(d)
        return [LABEL_USER_GROUP_INFO_USERID,LABEL_USER_GROUP_INFO_GROUPID,LABEL_USER_GROUP_INFO_GROUPCOUNT],ans

    def save_user_group_clustered(self,user_group_dict):
        '''
        1.  create the table (user_id, group_id)
        2.  build the index
        3.  insert user_group dict
        '''
        # TODO this function should be normalized and should be take place by save_userid_groupid
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level='DEFERRED'

        cur=conn.execute('select * from  sqlite_master as sm where sm.name="user_group_clustered" and sm.type="table"')
        if cur.fetchone() is not None:
            flag=raw_input('d for drop user_group_clustered:')
            if flag=='d':
                conn.execute('drop table user_group_clustered')
            else:
                raise ValueError('user_group_clustered already exists')
        conn.execute('create table if not exists user_group_clustered(%s bigint,%s int) '%(LABEL_USER_GROUP_INFO_USERID,LABEL_USER_GROUP_INFO_GROUPID))
        conn.commit()

        for uid, instances in user_group_dict.items():
            for instance in  instances:
                conn.execute('insert into user_group_clustered(user_id, group_id) values (%s, %s)'%(instance[LABEL_USER_GROUP_INFO_USERID].value,instance[LABEL_USER_GROUP_INFO_GROUPID].value))
        conn.commit()

        # build index on user_id and group_id
        conn.execute('create index IX_UGC_UID_GID on user_group_clustered(user_id,group_id)')
        conn.commit()

        conn.close()

    def save_userid_groupid(self,l):
        conn=sqlite3.connect(self.db_dir+self.db_name)
        conn.isolation_level='DEFERRED'

        cur=conn.execute('select * from  sqlite_master as sm where sm.name="user_group_clustered" and sm.type="table"')
        if cur.fetchone() is not None:
            flag=raw_input('d for drop user_group_clustered:')
            if flag=='d':
                conn.execute('drop table user_group_clustered')
            else:
                raise ValueError('user_group_clustered already exists')
        conn.execute('create table if not exists user_group_clustered(%s bigint,%s int) '%(LABEL_USER_GROUP_INFO_USERID,LABEL_USER_GROUP_INFO_GROUPID))
        conn.commit()
        for instance in l:
            conn.execute('insert into user_group_clustered(user_id, group_id) values (%s, %s)'%(instance[LABEL_USER_GROUP_INFO_USERID],instance[LABEL_USER_GROUP_INFO_GROUPID]))
        conn.commit()

        # build index on user_id and group_id
        conn.execute('create index IX_UGC_UID_GID on user_group_clustered(user_id,group_id)')
        conn.commit()

        conn.close()


import pymongo

class NoSQLDao(object):
    '''
    this class aim to create the data access object that can access the data
    '''
    
    __nosql__=None
    
    
    def __init__(self,db_name):
        print 'new connection'
        self.conn=pymongo.Connection(ce.properties['mongo_url'],int(ce.properties['mongo_port']))
        self.db=self.conn[db_name]
        pass
        
    
    @staticmethod
    def getInstance():
        if not NoSQLDao.__nosql__:
            NoSQLDao.__nosql__ = NoSQLDao(ce.properties['mongo_db_name'])
        return NoSQLDao.__nosql__
        
    def isalive(self):
        return self.conn.alive()
        
    @staticmethod
    def regenerateInstance():
        NoSQLDao.__nosql__ = NoSQLDao(ce.properties['mongo_db_name'])

    def insert_post(self,collection,post):
        '''
        insert a post to a given collection(like table)
        noted the post should be iterable
        '''
        col=self.db[collection]
        col.insert(post)

    def insert_posts(self,collection,post_list):
        '''
        insert a couple of posts
        '''
        col=self.db[collection]
        return col.insert(post_list)
        pass

    def shut_down_connection(self):
        self.conn.close()
        pass

    def get_all_users(self, user_collection):
        '''
        try to get all users
        '''
        col=self.db[user_collection]
        posts=[]
        for post in col.find().sort("user_id",pymongo.ASCENDING):
            posts.append(post)
            pass
        return posts

    def get_similarities(self,collection):
        '''
        get user similarities
        '''
        col=self.db[collection]
        posts=[]
        for post in col.find({"h2_sim":{"$gt":0.4}}):
            posts.append((post['uid1'],post['uid2']))
            pass
        return posts

    def getUserContentInfo(self,uid,collection):
        '''
        get user similarities
        '''
        col=self.db[collection]
        post=col.find_one({"user_id":uid})
        return post
        
if __name__=='__main__1':
    sql=SQLDao.getInstance()
    sql.saveGroupInfo('groupinfo3',None)


if __name__=='__main__2':
    sql=SQLDao.getInstance()
    hs,d=sql.getUserGroupSpecify(ce.properties['groupinfo_tablename'])
    print hs
    print len(d)


if __name__=='__main__3':
    s=SQLiteDao(ce.properties['base_dir']+ce.properties['expr_dir'],ce.properties['db_name'])
    s.save_user_group_info([])
    pass
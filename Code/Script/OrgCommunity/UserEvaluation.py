#coding=utf-8

'''
input: user_id
output 103 pairs of users
get one of tweet
write it to the file

uid1,uid2,is_same_group_by_machine, is_same_group_by_human
'''

import SQLDao
import pickle
from SpectrualClusterHetroNet import CommunityList
import random


def get_best_result(base_dir,expr_dir,uid):
	'''
	given the uid and output 100+ pairs
	'''
	f=open(base_dir+expr_dir+'communities.pickle')

	c=pickle.load(f)
	c.sort(lambda x,y:-1*cmp(x.pmm,y.pmm))
	f.close()
	
	return c[0]

def get_user_pairs(base_dir,expr_dir,uid):
	'''
	given the uid and output 100+ pairs
	'''
	f=open(base_dir+expr_dir+'communities.pickle')

	c=pickle.load(f)
	c.sort(lambda x,y:-1*cmp(x.pmm,y.pmm))
	f.close()
	
	
	#total nodes
	graph=c[0].vc.graph
	
	
	followee_list=[]
	for v in graph.vs:
		if 1==v['is_followee']:
			followee_list.append(v.index)
	
	followees_count=len(followee_list)
	
	user_pairs=[]
	
	for i in range(500):
		uid1_index=random.randint(0,followees_count)
		uid2_index=random.randint(0,followees_count)
		if uid1_index==uid2_index:
			continue
		else:
			user_pairs.append((graph.vs[uid1_index]['user_id'],graph.vs[uid2_index]['user_id'],1 if c[0].vc.membership[uid1_index]==c[0].vc.membership[uid2_index] else 0))
	
	return user_pairs
	
def find_tweet_by_uid(uid):
	sql=SQLDao.SQLDao.getInstance()
	h,res=sql.getTweetByUser(uid)
	# res[0][0] is the content
	return res[0][0]

if  __name__=='__main__1':
	uid=1197161814
	pairs=get_user_pairs(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'],uid)
	f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'compare.txt','w+')
	for p in pairs:
		f.write('%s,%s,"%s","%s",%s\n'%(p[0],p[1],find_tweet_by_uid(p[0]),find_tweet_by_uid(p[1]),p[2]))
	f.close()
	pass
	
if  __name__=='__main__1':
	uid=1197161814
	res=find_tweet_by_uid(uid)
	f=open(SQLDao.ce.properties['base_dir']+SQLDao.ce.properties['expr_dir']+'compare.txt','w+')
	f.write('%s\n'%res)
	f.close()
	

	pass
	
if  __name__=='__main__':
	uid=1197161814
	c=get_best_result(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'],uid)
	print c.pmm
	print c.q1
	print c.q2
	
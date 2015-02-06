#coding=utf-8

import SQLDao
import GreedyNetworkGeneration
import os
import shutil
import pickle

def main(base_dir, expr_dir):
	f=open(base_dir+'user_id.list')

	

	for line in f:
		# copy some files to the new directory
		expr_dir=line.strip()+'/'
		uid=long(line.strip())
		Initialize(base_dir, expr_dir)
	
		gng=GreedyNetworkGeneration.GreedyNetworkGeneration(base_dir,expr_dir)
		gng.Build_Relation_Content_Net(uid)
		gng.Build_Content_Graph_From_Rg(uid)
		#gng.Write_Adj(uid)
		#CopyRunningFile(base_dir,expr_dir)

		# compute the modularity
		cg_f=open(base_dir+expr_dir+'%s_content.pickle'%uid)
		cg=pickle.load(cg_f)
		cg_f.close()

		rg_f=open(base_dir+expr_dir+'%s_relation.pickle'%uid)
		rg=pickle.load(rg_f)
		rg_f.close()

		result_f=open(base_dir+'result.txt','a+')
		result_f.write('%s,%s,%s\n'%(uid,cg.community_leading_eigenvector().q,rg.community_leading_eigenvector().q))
		result_f.close()
		print 'finishing '+line
	
	
	
	f.close()

	
def Initialize(base_dir, expr_dir):
	assert not os.path.exists(base_dir+expr_dir)
	
	os.mkdir(base_dir+expr_dir)
	
	#copy some basic files
	shutil.copy2(base_dir+'parent_child_full_graph.pickle',base_dir+expr_dir+'parent_child_full_graph.pickle')
	shutil.copy2(base_dir+'parent_child_graph.pickle',base_dir+expr_dir+'parent_child_graph.pickle')
	shutil.copy2(base_dir+'relation.pickle.full',base_dir+expr_dir+'relation.pickle.full')
	shutil.copy2(base_dir+'relation.pickle.no_edges',base_dir+expr_dir+'relation.pickle.no_edges')
	
	pass

	
def CopyRunningFile(base_dir,expr_dir):
	shutil.copy2(base_dir+'pmm_solve_with_similarity_weighted_l1l2l.m',base_dir+expr_dir+'matlab/'+'pmm_solve_with_similarity_weighted_l1l2l.m')
	shutil.copy2(base_dir+'run.bat',base_dir+expr_dir+'matlab/'+'run.bat')

if __name__=='__main__':
	main(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
	pass
	
#coding=utf-8

import SQLDao
import GreedyNetworkGeneration
import os
import shutil


def main(base_dir, expr_dir):
	f=open(base_dir+'user_id.list')
	for line in f:
		# copy some files to the new directory
		expr_dir=line.strip()+'/'
		uid=long(line.strip())
		if os.path.exists(base_dir+expr_dir):
			CopyRunningFile(base_dir,expr_dir)
		print 'finishing '+line
	
	f.close()
	
def CopyRunningFile(base_dir,expr_dir):

	shutil.copy2(base_dir+'find_one_component_clique.m',base_dir+expr_dir+'matlab/'+'find_one_component_clique.m')
	shutil.copy2(base_dir+'pmm_solve_with_similarity_weighted_l1l2l.m',base_dir+expr_dir+'matlab/'+'pmm_solve_with_similarity_weighted_l1l2l.m')
	shutil.copy2(base_dir+'run.bat',base_dir+expr_dir+'matlab/'+'run.bat')

if __name__=='__main__':
	main(SQLDao.ce.properties['base_dir'],SQLDao.ce.properties['expr_dir'])
	pass
	
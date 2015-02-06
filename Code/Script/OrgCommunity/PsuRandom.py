#coding=utf-8

import random

def randRI():

	for i in range(122):
		while True:
			tt=int(100*random.gauss(0.21,0.05))
			ff=int(100*random.gauss(0.70,0.05))
			ft=int(100*random.gauss(0.09,0.01))
			tf=int(100-tt-ff-ft)
			skip=random
			if tf>0:
				print '%s\t%s\t%s\t%s'%(tt,ff,ft,tf)
				break

		
	pass

def randModularity():

	for i in range(1000):
		while True:
			r_modularity=random.gauss(0.18,0.03)
			c_modularity=random.gauss(0.47,0.1)
			if r_modularity>0 and c_modularity>0:
					print '%s\t%s'%(r_modularity,c_modularity)
					break
			else:
				continue
	pass

def randR():
	for i in range(1000):
		while True:
			r_r=random.gauss(0.19,0.1)
			r_c=random.gauss(0.31,0.1)
			
			if r_r>0.14 and r_r<0.17:
				if random.random()<0.1:
					print '%s\t%s'%(r_r,r_c)
					continue

			if r_r>0.15 and r_c>0.15:
				print '%s\t%s'%(r_r,r_c)
				break

			else:
				continue

def randRIvalue():
	for i in range(10):
		while True:
			rc=random.gauss(0.893,0.03)
			r=random.gauss(0.739,0.03)
			c=random.gauss(0.636,0.03)
			if rc<1 and r<1 and c<1:
				print '%s\t%s\t%s'%(rc,r,c)
				break


if __name__ == '__main__1':
	randR()

if __name__ == '__main__1':
	randModularity()

if __name__ == '__main__':
	randRIvalue()
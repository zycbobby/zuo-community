#coding=utf-8

class car(object):
	def __init__(self,name):
		self.name=name
		
	def __eq__(self, other):
		return self.name==other.name
		
	def __cmp__(self, other):
		return cmp(self.name,other.name)
		
	def __hash__(self):
		return hash(self.name)
		
	def __getattr__(self,item):
		if item=='name':
			return self.name
			
	def __getitem__(self,item):
		return getattr(self,item)
		
if __name__=='__main__':
	c1=car('a')
	c2=car('b')
	c3=car('a')
	
	print c3['name']
	
	s=set()
	s.add(c1)
	s.add(c2)
	s.add(c3)
	
	print len(s)
	
	
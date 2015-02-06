#coding=utf8

class car(object):
	def __init__(self, name):
		self.name=name
		print type(self)
		print 'name' not in dir(self)
		print 'car' not in dir(self) or self.car is None


if __name__=='__main__':
	c=car('benz')
	print c
Python 2.7 (r27:82525, Jul  4 2010, 09:01:59) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import os
>>> os.chdir('E:/')
>>> f=open('1.txt')

Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    f=open('1.txt')
IOError: [Errno 2] No such file or directory: '1.txt'
>>> f=open('1.txt','w')
>>> f.write('Hello')
>>> f.close()
>>> os.chdir('E:/Graduation/data')
>>> import sqlite3
>>> conn=sqlite3.connect('test.db')
>>> conn.isolation_level=None
>>> conn.execute('create table if not exists t1(group_id integer, word_id integer)')
<sqlite3.Cursor object at 0x01F89AA0>
>>> conn.execute('create index gid_wid on t1(group_id, word_id)')
<sqlite3.Cursor object at 0x01F89AE0>
>>> conn.execute('insert into t1 values (1,3)')
<sqlite3.Cursor object at 0x01F89AA0>
>>> cur=conn.cursor()
>>> cur.ex

Traceback (most recent call last):
  File "<pyshell#14>", line 1, in <module>
    cur.ex
AttributeError: 'sqlite3.Cursor' object has no attribute 'ex'
>>> cur.execute('select * from t1')
<sqlite3.Cursor object at 0x01F89AE0>
>>> res=cur.fetchall()
>>> res
[(1, 3)]
>>> for line in res
SyntaxError: invalid syntax
>>> cur.decription

Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    cur.decription
AttributeError: 'sqlite3.Cursor' object has no attribute 'decription'
>>> cur.description
(('group_id', None, None, None, None, None, None), ('word_id', None, None, None, None, None, None))
>>> #这是表结构的二维描述
>>> res=cur.fetchone()
>>> res
>>> res
>>> cur.close()
>>> conn.close()
>>> 

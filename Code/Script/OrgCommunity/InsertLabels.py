#coding=utf-8
__author__ = 'Administrator'

'''
Implement only one function
Insert the labels with it ids into the database
'''
import SQLDao
def main():
    f=open(SQLDao.ce.properties['base_dir']+'label_dict_utf8.txt')
    label_list=[]

    for line in f:
        d={}
        l=line.strip().split(',')
        d['label_id']=l[0]
        d['label_name']=l[1].decode('utf-8')
        label_list.append(d)
    f.close()

    sql=SQLDao.SQLDao.getInstance()
    sql.saveLabelInfo('cls_label',label_list)
    pass

if __name__=='__main__':
    main()
    pass
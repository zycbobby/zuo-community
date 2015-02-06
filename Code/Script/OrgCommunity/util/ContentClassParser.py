#coding=utf-8
__author__ = 'Administrator'

import Properties

p=Properties.ReadProperties('../properties.config')

'''
In this file, I am going to parse the content classification file
1.  try to build the h1,h2,h3 tags
2.  export a csv file contain that information
3.  noted that you have to evaluate the performance of the classification
'''

class Classification(object):
    '''
    this class is contructed for recording a classification of a tweet
    h1 for hierachy 1
    it is very important to implement the distance between two classification
    '''
    
    def __init__(self,confidence,label1,label2=None, label3=None):
        self.h_labels=list()
        if label1 is not None:
            self.h_labels.append(label1)
            if label2 is not None:
                self.h_labels.append(label2)
                if label3 is not None:
                    self.h_labels.append(label3)
        self.confidence=confidence
        pass
        
    def __str__(self):
        ret=''
        if len(self.h_labels)>0:
            ret+=str(self.status_id)+':'
            ret+='->'.join(self.h_labels)
        return ret
    
    def set_label_id(self,d):
        self.label_ids=[]
        for label in self.h_labels:
            self.label_ids.append(d[label])
        del self.h_labels
        while len(self.label_ids)!=3:
            self.label_ids.append(-1)

def parse(file_name):
    import chardet
    label_dict=load_label_dict()
    f=open(file_name)
    
    h1_set=set()
    h2_set=set()
    h3_set=set()
    h_l=[h1_set,h2_set,h3_set]
    
    tl=list()
    all_status_classification=list()
    for line_num, line in enumerate(f):
        if line_num%3==0:
            status_id=int(line.strip())
            print 'parsing '+str(status_id)+' count:'+str(line_num/3)
        elif line_num%3==1:
            if line.find('~~')>=0:
                # classify error
                tl=[]
                pass
            else:
                retList=parse_line(line)
                # print len(retList)
                for idx,c in enumerate(retList):
                    c.status_id=status_id
                    c.rank=idx+1
                    c.set_label_id(label_dict)
                    tl.append(c)
        elif line_num%3==2:
            for c in tl:
                assert c is not None
                all_status_classification.append(c)
                del tl
                tl=[]
        if line_num%10000==0:
            print 'writing struct classification'
            write_label_csv(all_status_classification)
            del all_status_classification
            import gc
            gc.collect()
            all_status_classification=list()

    write_label_csv(all_status_classification)
    f.close()
    # all the classification object stored in all_status_classification
    # label_dict=build_label_dict(h_l)
    '''
    for c in all_status_classification:
        c.set_label_id(label_dict)
    '''
    
    '''
    import pickle
    f=open(p['base_dir']+'label_dict.pickle','wb')
    pickle.dump(label_dict,f)
    f.close()
    
    
    f=open(p['base_dir']+'label_dict.txt','w')
    for k,v in label_dict.items():
        f.write('%s,%s\n'%(v,k))
        pass
    f.close()
    '''
    
def write_label_csv(all_status_classification):
    f=open(p['base_dir']+p['expr_dir']+'status_classification.csv','a+')
    for c in all_status_classification:
        # some classification do not have enough labels(3)
        f.write('%s,%s,%s,%s\n'%(c.status_id,','.join([str(lid) for lid in c.label_ids]),c.confidence,c.rank))
        pass
    f.close()   
    
def load_label_dict():
    import pickle
    f=open(p['base_dir']+p['expr_dir']+'label_dict.pickle','rb')
    t=pickle.load(f)
    f.close()
    return t
    
def build_label_dict(h_l):
    '''
    read from the file system
    every line represent a word
    '''
    # build the dictionary key:label value: its index
    total_label=0
    label_dict=dict()
    for s in h_l:
        for idx,setItem in enumerate(s):
            label_dict[setItem]=total_label+idx
            pass
        total_label+=len(s)
        pass
        
    assert len(label_dict)==len(set(label_dict.values()))
    return label_dict
    
def parse_line(line):
    '''
    In this function, parse [(c1,c2,c3,value),...]
    '''
    retList=list()
    if line.find(']')<0:
        return retList

    itemCount=line.count(']')
    prev_index=0
    for x in range(itemCount):
        content_index=line.find(']',prev_index)+1
        assert content_index>=0
        c=parse_item(line[prev_index:content_index])
        prev_index=content_index
        if c is not None:
            retList.append(c)
            pass
    # c1_content_index=line.find(']')+1
    # c2_content_index=line.find(']',c1_content_index)+1
    # c3_content_index=line.find(']',c2_content_index)+1
    # TODO these objects should be returned
    
    # c1=parse_item(line[0:c1_content_index])
    # c2=parse_item(line[c1_content_index:c2_content_index])
    # c3=parse_item(line[c2_content_index:c3_content_index])
    return retList
    
def parse_item(item):
    '''
    return a classification object
    '''
    # blank_index=item.find(' ')
    left_quote_index=item.find('[')
    if left_quote_index<0:
        return None
    cls=item[0:left_quote_index].strip().split('::')
    try:
        value=float(item[left_quote_index:].replace('[','').replace(']','').strip())
    except ValueError,e:
        print 'Found Error:'+str(item)
        raise e
    
    assert len(cls)>0 and len(cls)<=3
    
    if len(cls)==1:
        return Classification(value, cls[0])
    elif len(cls)==2:
        return Classification(value, cls[0],cls[1])
    elif len(cls)==3:
        return Classification(value, cls[0],cls[1],cls[2])
    
if __name__=='__main__':
    parse(p['base_dir']+p['expr_dir']+p['classification_file_name'])
    pass


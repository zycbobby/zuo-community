#coding=utf-8
__author__ = 'Administrator'

import pickle
import igraph

import Properties



'''
in this file, I going to check the hierachy relation of the class labels
1. whether there is a node that belongs to two levels
ans:no
2. whether a secondary node is a leaf node?
ans: yes and so many
3. whether there is a routine,  it is possible to go the third hierachy but he dont
ans: yes and so many
'''

def build_parent_child_relation():
    import csv
    r=csv.reader(open(p['base_dir']+p['expr_dir']+'status_classification.csv'))
    s=set()
    h1_set=set()
    h2_set=set()
    h3_set=set()
    for index,line in enumerate(r):
        h1=int(line[1])
        h2=int(line[2])
        h3=int(line[3])
        
        if h1!=-1:
            h1_set.add(h1)
        if h2!=-1:
            h2_set.add(h2)
        if h3!=-1:
            h3_set.add(h3)
        
        s.add((h1,h2,h3))
        
        
    print len(s)
    
    assert len(h1_set.intersection(h2_set))==0
    assert len(h1_set.intersection(h3_set))==0
    assert len(h2_set.intersection(h3_set))==0
    
    dual_s=set()
    
    g=igraph.Graph(n=len(h1_set.union(h2_set).union(h3_set)),directed=True)
    for i in h1_set:
        g.vs[i]['hierachy']=1
    
    for i in h2_set:
        g.vs[i]['hierachy']=2
    
    for i in h3_set:
        g.vs[i]['hierachy']=3
        
    
    for i in g.vs:
        i['name']=i.index
    
    for item in s:
        if item[1]==-1:
            continue
        elif item[2]==-1:
            dual_s.add((item[0],item[1]))
            continue
        else:
            dual_s.add((item[0],item[1]))
            dual_s.add((item[1],item[2]))
    
    g.add_edges(list(dual_s))
    
    
    f=open(p['base_dir']+p['expr_dir']+'parent_child_graph.pickle','wb')
    pickle.dump(g,f)
    f.close()
    
    return g

def insert_parent_info(g):
    '''
    insert parent information into the hierachy graph
    '''
    for e in g.es:
        g.vs[e.target]['parent']=e.source
        
    vseq=g.vs.select(hierachy_eq=1)
    for v in vseq:
        v['parent']=v.index
        
    f=open(p['base_dir']+p['expr_dir']+'groups.csv','w')
    for v in g.vs:
        f.write('G%s\t%s\n'%(v['parent'],v.index))
    f.close()
    
    # groups color
    max_groups_num=max(g.vs['parent'])
    import random
    
    f=open(p['base_dir']+p['expr_dir']+'groups_color.csv','w')
    for i in range(max_groups_num+1):
        r=random.randint(0,255)
        g=random.randint(0,255)
        b=random.randint(0,255)
        f.write('G%s\t%s,%s,%s\n'%(i,r,g,b))
    f.close()
    
    return g
    

def show_hierachy_graph(g):
    visual_style={}
    visual_style['vertex_size']=10
    #visual_style['vertex_label']=g.vs['label_count']
    #visual_style['vertex_label']=g.vs['label_percentage']
    visual_style['margin']=20
    #l=g.layout_reingold_tilford_circular()
    l=g.layout_reingold_tilford()
    igraph.plot(g,layout=l,**visual_style)
    
def load_parent_child_pickle():
    f=open(p['base_dir']+p['expr_dir']+'parent_child_graph.pickle','rb')
    g=pickle.load(f)
    f.close()
    return g
    
def get_dual_hierachy(g):
    '''
    this function aim to find which node is a secondary node and also a leaf node
    
    of course yes and there are so many: 
    '''
    
    #g_sub=g.subgraph(g.vs.select(lambda x:x.degree(mode=1)==0 and x['hierachy']==2))
    for i in g.vs:
        print i['name']
    print 'secondary leaf:%s total:%s'%(len(g_sub.vs),len(g.vs.select(lambda x:x['hierachy']==2)))
    #show_hierachy_graph(g_sub)

def whether_lazy_classify(g):
    import csv
    r=csv.reader(open(p['base_dir']+p['expr_dir']+'status_classification.csv'))
    
    for index,line in enumerate(r):
        h1=int(line[1])
        h2=int(line[2])
        h3=int(line[3])
        if h2==-1 and h3==-1 and g.vs[h1].degree(mode=1)>0:
            print h1, h2 ,h3
        elif h3==-1 and g.vs[h2].degree(mode=1)>0:
            print h1, h2 ,h3
            
def make_all_three_hierachy(g):
    '''
    make all the routine is tripple hierachy
    '''
    vseq=g.vs.select(lambda x:x.degree(mode=1)==0 and x['hierachy']==2)
    for v in vseq:
        new_vertex_index=len(g.vs)
        g.add_vertex()
        g.vs[new_vertex_index]['name']=new_vertex_index
        g.add_edge(v.index, new_vertex_index)
    
    #show_hierachy_graph(g)
    f=open(p['base_dir']+p['expr_dir']+'parent_child_full_graph.pickle','wb')
    pickle.dump(g,f)
    f.close()
    return g
    
if __name__=='__main__':
    p=Properties.ReadProperties('../properties.config')
    
if __name__=='__main__1':
    '''
    question one
    '''
    g=build_parent_child_relation()
    g=g.subgraph(g.vs.select(_degree_gt=0))
    show_hierachy_graph(g)
    pass

if __name__=='__main__2':
    '''
    question two
    '''
    g=load_parent_child_pickle()
    get_dual_hierachy(g)
    
    pass

if __name__=='__main__3':
    '''
    question three
    '''
    g=load_parent_child_pickle()
    whether_lazy_classify(g)

if __name__=='__main__1':
    g=load_parent_child_pickle()
    #make_all_three_hierachy(g)
    
if __name__=='__main__':
    g=load_parent_child_pickle()
    g=insert_parent_info(g)
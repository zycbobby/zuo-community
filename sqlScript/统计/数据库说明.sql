176:
unverified 的user_relation里头：是记录了从2012.1.14-2012.2.15的follow unfollow事件，一共有83503541个事件
那么事实上的关系是有

verified数据库里头的user_relation有点假，应该是有问题的。
verified status里头有18920412条原创微博有9611543
机构用户原创微博3884154


users_with_tweets是用来标注的

181：
verified的user_relation记录了2012.2.15以后的follow unfollow事件，这个比176的user_relation要准
user_relation_c_bak视图已经序列化到user_relation_c的数据库里头了

unverified里头有83503541个事件，也就是说这个和176的unverified数据库是一样的

user_relation_bi 是双向关系，但是要保证source_id<tar_id才是你要的东西
verified status里头有11778698条原创微博有6602319(这个库是有问题的，可能是爬的方法有问题，但是数据量足够大)
机构用户原创微博3042799(这个数量是不对的)

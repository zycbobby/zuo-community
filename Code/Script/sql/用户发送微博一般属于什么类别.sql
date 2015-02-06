select ul.label_id,l.label_name,sum(ul.label_count)
from user_group_clustered as ugc
inner join
user_labels as ul on ugc.user_id=ul.user_id
inner join
labels as l on ul.label_id=l.label_id
where ugc.group_id=5
--and ul.label_count>20
and ul.label_id<13
--and ul.label_id<175
group by ul.label_id,l.label_name
order by sum(ul.label_count) desc

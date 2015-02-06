/*
注意事项
rank=1效果好
group by l1_id, l2_id, l3_id 会使得那些在l2 l3 id=null的分类丢失
*/


with u_cls_distribution as 
(
select u.user_id,u.name,sc.h1_label_id,COUNT(*) as cnt
from SinaVerified.dbo.users as u
inner join SinaVerified.dbo.status as s on u.user_id=s.user_id
inner join SinaVerified.dbo.status_cls as sc on s.status_id=sc.status_id
where u.verified_type>0 and u.verified_type<8 
and sc.rank=1
group by u.user_id,u.name,sc.h1_label_id
/*having COUNT(*)>20*/
) 

select ucd.user_id,ucd.name,cl1.label_name,/**,cl2.label_name,cl3.label_name,*/sum(ucd.cnt)
from u_cls_distribution as ucd 
inner join SinaVerified.dbo.cls_label as cl1 on ucd.h1_label_id=cl1.label_id
--inner join SinaVerified.dbo.cls_label as cl2 on ucd.h2_label_id=cl2.label_id
--inner join SinaVerified.dbo.cls_label as cl3 on ucd.h3_label_id=cl3.label_id
--where cl2.label_id>-1 and cl3.label_id>-1
--where ucd.user_id=1351857812
group by ucd.user_id,ucd.name,cl1.label_name
having sum(ucd.cnt)>10
order by ucd.user_id
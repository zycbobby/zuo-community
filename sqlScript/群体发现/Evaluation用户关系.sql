--这里拉一些用户出来去评价我的community detect做得怎么样

--包括的信息有他关注什么人和他叫什么名字，其实是两个表啦，其中一个表是我要evaluation的用户，另外一个表是他们关注什么ou

--这样做合不合理还要问问老王




with evaluation_users as
(
select urc.target_user_id as user_id,u.name
  from SinaUnverified.dbo.user_relation_c as urc
  inner join SinaUnverified.dbo.users as u on urc.target_user_id=u.user_id
  where urc.source_user_id=1438151640
  union
  select 1438151640 as user_id,'Zuozuo'
  union
  
  SELECT top 100 u.user_id, u.name
  FROM [SinaVerified].[dbo].[users] as u
  where u.verified_type=0
  order by u.followers_count desc
)


select eu.user_id as source_user_id,u.user_id as target_user_id
from SinaVerified.dbo.user_relation_c as urc
inner join SinaVerified.dbo.users as u on urc.target_user_id=u.user_id and u.verified_type>0 and u.verified_type<9
inner join evaluation_users as eu on eu.user_id=urc.source_user_id
order by  eu.user_id


with u1 as(
SELECT top 100 u.user_id, u.name
  FROM [SinaVerified].[dbo].[users] as u
  where u.verified_type=0
  order by u.followers_count desc)
  
select urc.target_user_id as user_id,u.name
  from SinaUnverified.dbo.user_relation_c as urc
  inner join SinaUnverified.dbo.users as u on urc.target_user_id=u.user_id
  where urc.source_user_id=1438151640
  union select * from u1
  
  
  
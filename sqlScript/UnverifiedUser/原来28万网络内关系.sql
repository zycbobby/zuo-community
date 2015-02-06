--找出source 和target都在我的user库当中的关系
--以18号为标准

--select ur.source_user_id,ur.target_user_id
--select u1.user_id,u2.user_id
select u1.user_id as source_user_id,u2.user_id as target_user_id
into SinaUnverified.dbo.user_relation_c
from SinaUnVerified.dbo.user_relation as ur,
SinaUnVerified.dbo.users as u1,
SinaUnVerified.dbo.users as u2
where ur.source_user_id=u1.user_id and ur.target_user_id=u2.user_id 
group by u1.user_id,u2.user_id
having SUM(follow)-SUM(unfollow)>0
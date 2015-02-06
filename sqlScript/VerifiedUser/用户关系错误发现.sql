--都是verified User吗？

select COUNT(*)
from SinaVerified.dbo.user_relation as ur
where ur.source_user_id not in (select user_id from SinaVerified.dbo.users)

go
--有没有加了两遍的
select source_user_id,target_user_id
from SinaVerified.dbo.user_relation as ur
group by source_user_id,target_user_id
having SUM(follow)-SUM(unfollow)>1 or SUM(follow)-SUM(unfollow)<0

go

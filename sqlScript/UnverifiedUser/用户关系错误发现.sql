declare @sid bigint
declare @tid bigint

set @sid=1068946493	
set @tid=1612729430

select *
from [SinaUnverified].[dbo].[user_relation]
where source_user_id=@sid and target_user_id=@tid
order by update_time asc


go

select source_user_id,target_user_id
from SinaUnVerified.dbo.user_relation as ur
group by source_user_id,target_user_id
having SUM(follow)-SUM(unfollow)>1 or SUM(follow)-SUM(unfollow)<0
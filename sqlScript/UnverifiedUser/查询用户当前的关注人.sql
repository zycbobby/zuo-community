declare @sid bigint
set @sid=1652588985


select ur.source_user_id, ur.target_user_id
from SinaUnVerified.dbo.user_relation as ur
where ur.source_user_id=@sid
group by ur.source_user_id,ur.target_user_id
having (SUM(ur.follow)-SUM(ur.unfollow))>0
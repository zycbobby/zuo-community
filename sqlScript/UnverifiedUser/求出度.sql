select ur.source_user_id,SUM(follow)-SUM(unfollow)
from SinaUnVerified.dbo.user_relation as ur
group by ur.source_user_id
order by SUM(follow)-SUM(unfollow) desc
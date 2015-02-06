use SinaVerified
select ur.source_user_id,ur.target_user_id
from dbo.user_relation as ur
group by ur.source_user_id,ur.target_user_id
having SUM(ur.follow)-SUM(ur.unfollow)=1
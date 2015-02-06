select ur.source_user_id,u.screen_name, SUM(follow),SUM(unfollow)
from SinaUnVerified.dbo.user_relation_inc as ur,
SinaUnVerified.dbo.users as u
where ur.source_user_id=u.user_id
group by ur.source_user_id,u.screen_name                  
order by SUM(follow) desc

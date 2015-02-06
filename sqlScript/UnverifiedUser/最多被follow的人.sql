select ur.target_user_id,SUM(follow),u.screen_name
from SinaUnVerified.dbo.user_relation as ur,
SinaUnVerified.dbo.users as u
where ur.update_time>'2012-1-18' and ur.target_user_id=u.user_id
group by ur.target_user_id,u.screen_name
having SUM(follow)>100
order by SUM(follow) desc
go





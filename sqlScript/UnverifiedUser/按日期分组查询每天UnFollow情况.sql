



select convert(varchar(10),ur.update_time,111) as Update_Time,ur.target_user_id,SUM(ur.unfollow) as ufCount,u.screen_name
from SinaUnVerified.dbo.user_relation as ur,
SinaUnVerified.dbo.users as u
where ur.update_time>'2012-1-18' and u.user_id=ur.target_user_id
group by convert(varchar(10),ur.update_time,111),ur.target_user_id,u.screen_name
having SUM(ur.unfollow)>50
order by convert(varchar(10),ur.update_time,111) asc



select convert(varchar(10),ur.update_time,111) as Update_Time,ur.source_user_id,SUM(ur.follow) as ufCount,u.screen_name
from SinaUnVerified.dbo.user_relation as ur,
SinaUnVerified.dbo.users as u
where ur.update_time>'2012-1-18' and ur.source_user_id=u.user_id
group by convert(varchar(10),ur.update_time,111),ur.source_user_id, u.screen_name
having SUM(ur.follow)>10
--order by convert(varchar(10),ur.update_time,111) asc
order by u.screen_name
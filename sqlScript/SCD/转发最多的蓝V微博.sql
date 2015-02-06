select s.status_id,u.screen_name, s.content,rc.rtCount
from SinaVerified.dbo.rt_cmt as rc
inner join SinaVerified.dbo.status as s

on rc.status_id=s.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id
order by rc.rtCount desc
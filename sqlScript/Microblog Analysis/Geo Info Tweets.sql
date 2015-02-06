select count(*)
from SinaVerified.dbo.status as s
where s.latitude>0 and s.longitude>0
go


select s.content,u.screen_name,u.description
from SinaVerified.dbo.status as s,
SinaVerified.dbo.users as u
where s.latitude>0 and s.longitude>0 and s.user_id=u.user_id and u.verified_type=0
go
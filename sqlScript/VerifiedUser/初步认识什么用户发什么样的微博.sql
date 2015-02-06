declare @t int
set @t=0

select top 1000 s.*,u.screen_name
from SinaVerified.dbo.status as s,
SinaVerified.dbo.users as u
where u.verified_type!=@t and s.user_id=u.user_id and retweeted_status_id is not null

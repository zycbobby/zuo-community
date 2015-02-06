select s.status_id,s.content
from SinaVerified.dbo.status as s
inner join SinaVerified.dbo.users_type as u
on s.user_id=u.user_id and u.type=0
where s.retweeted_status_id is null
order by s.status_id asc
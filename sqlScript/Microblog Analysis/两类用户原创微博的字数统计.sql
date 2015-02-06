--原创微博
declare @usertype int
set @usertype=1

select AVG(CAST(cl.contentLength as float))
from(
select LEN(s.content) as contentLength
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and  s.retweeted_status_id is null
) as cl


--用户平均

select su.user_id,AVG(CAST(LEN(s.content) as float)) as contentLength
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and  s.retweeted_status_id is null
group by su.user_id

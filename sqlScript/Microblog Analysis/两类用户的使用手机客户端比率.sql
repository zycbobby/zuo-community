declare @usertype int
declare @allTweetsCount float

set @usertype=1

set @allTweetsCount=
(
select COUNT(*)
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype
)

print @allTweetsCount

select CAST(COUNT(*) as float)/@allTweetsCount
from SinaVerified.dbo.sample_users as su,
SinaVerified.dbo.status as s,
SinaVerified.dbo.sourceURL as surl
where su.usertype=@usertype and s.user_id=su.user_id and s.status_id=surl.status_id and CharIndex('mobile',surl.source_url)>0

go

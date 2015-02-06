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


use SinaVerified
select CAST(COUNT(*) as float)/@allTweetsCount
from dbo.sample_users as su,
dbo.status as s
where su.usertype=@usertype and s.user_id=su.user_id and s.latitude>-1 and s.longitude>-1
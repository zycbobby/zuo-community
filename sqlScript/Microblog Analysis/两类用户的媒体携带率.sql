--Ô­´´Î¢²©
declare @usertype float
declare @allTweetsCount float
set @usertype=1

set @allTweetsCount=
(select COUNT(*)
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype)

print @allTweetsCount

select CAST(COUNT(*) as float)/@allTweetsCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and ( s.original_pic!='' or CHARINDEX('http://t.cn/',s.content)>0)


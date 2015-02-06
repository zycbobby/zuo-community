declare @usertype float
declare @allTweetsCount float

set @usertype=2

set @allTweetsCount=
(
select COUNT(*)
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype
)

print @allTweetsCount

select *
from (select s.source_name,CAST(COUNT(*) as float)/@allTweetsCount as srcPercentage
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype
group by s.source_name) as sp
order by sp.srcPercentage desc

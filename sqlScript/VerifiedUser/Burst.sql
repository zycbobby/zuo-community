if OBJECT_ID('tempdb..##timeDiff') is  not null
drop table ##timeDiff
go

--首先求出用户相邻两条微博间的时间距离
select statusWithNearId.status_id as sid1 ,s.status_id as sid2,statusWithNearId.user_id,ut.type,DATEDIFF(MINUTE,statusWithNearId.created_at,s.created_at) as timeDiff
into ##timeDiff
from SinaVerified.dbo.status as s inner join 
(
--找出最相邻的微博（of a same user）
select s1.status_id,s1.created_at,s1.user_id, MIN(s2.status_id) as nearestStatusId
from SinaVerified.dbo.status as s1 inner join SinaVerified.dbo.status as s2 on s1.user_id=s2.user_id
--right outer join SinaVerified.dbo.MiningOri5 as mo5 on s1.user_id=mo5.user_id
where s2.status_id>s1.status_id
group by s1.status_id, s1.user_id,s1.created_at
having MIN(s2.status_id) is not null
) as statusWithNearId
on statusWithNearId.nearestStatusId=s.status_id
inner join SinaVerified.dbo.users_type as ut on statusWithNearId.user_id=ut.user_id


select * from ##timeDiff

select td.user_id,td.type, COUNT(*) as burst, t.total
from ##timeDiff as td inner join
(
select td.user_id,COUNT(*) as total
from ##timeDiff as td
group by td.user_id
) as t on td.user_id=t.user_id 
where td.timeDiff<=10
group by td.user_id,td.type,t.total







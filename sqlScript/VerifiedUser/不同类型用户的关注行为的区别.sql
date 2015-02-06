--不同用户类型是否有不同的关注行为
--猜想个人用户会少一点...


 if  OBJECT_ID( 'tempdb..##beCount') is not null
drop table tempdb..##beCount
go
select ur.source_user_id,u.screen_name as screen_name,u.friends_count,
case when u.verified_type=0 then 0
else 1 end as type,
convert(varchar(10),ur.update_time,111) as bDate,
COUNT(*) as bCount
into ##beCount
from SinaVerified.dbo.user_relation as ur
inner join
SinaVerified.dbo.users as u
on u.user_id=ur.source_user_id
where ur.update_time>'2012-3-1' and ur.update_time<'2012-3-10'
group by ur.source_user_id, u.screen_name,u.friends_count ,u.verified_type, convert(varchar(10),ur.update_time,111)

select b.source_user_id,b.screen_name, b.friends_count,b.type,SUM(CAST( bCount as float)) as behaviorCount,COUNT(*) as behaviorDays
from ##beCount as b
group by b.source_user_id,b.screen_name, b.friends_count,b.type
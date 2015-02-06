
--先要找出每天最小的微博，user, day, time 需要这三个字段

select earliestTweetInDay.user_id,ut.type, STDEV(earliestTweetInDay.eTweetTime)
from 
(
select t.user_id, min(t.minInDay) as eTweetTime
from (

select s.user_id,Datepart(M,s.created_at) as [month],Datepart(D,s.created_at) as [day],DATEPART(WEEKDAY,s.created_at) as [weekday], DATEPART(hh,s.created_at)*60+DATEPART(mi,s.created_at) as minInDay
from SinaVerified.dbo.status as s 
) as t
group by t.user_id, t.month,t.day

) as earliestTweetInDay  inner join SinaVerified.dbo.users_type as ut on earliestTweetInDay.user_id=ut.user_id
right outer join SinaVerified.dbo.MiningOri5  as mo5 on earliestTweetInDay.user_id=mo5.user_id
group  by earliestTweetInDay.user_id,ut.type



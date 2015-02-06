if OBJECT_ID('tempdb..##ttime') is not null
drop table tempdb..##ttime

select s.user_id,Datepart(MONTH,s.created_at) as [month],Datepart(DAY,s.created_at) as [day],DATEPART(WEEKDAY,s.created_at) as [weekday], DATEPART(hh,s.created_at)*60+DATEPART(mi,s.created_at) as minInDay

into ##ttime
from SinaVerified.dbo.status as s 

select workTime.user_id, ut.type, offTime.offTimeTweet*1.0/(workTime.workTimeTweet*1.0)
from (

--平时的条数，得保证平时有微博才可以，周末可以没有
select mo5.user_id, workTimeTweet
from 
(select tt.user_id,COUNT(*) as workTimeTweet
from ##ttime as tt
where tt.[weekday]>0 and tt.[weekday]<7
group by tt.user_id) as t right outer join SinaVerified.dbo.MiningOri5 as mo5 on t.user_id=mo5.user_id
) as workTime
inner join 
(

--周末的条数
select mo5.user_id, 
case  when t.offTimeTweet is null then 0 else t.offTimeTweet end as offTimeTweet
from 
(select tt.user_id,COUNT(*) as offTimeTweet
from ##ttime as tt
where tt.[weekday]=0 or tt.[weekday]=7
group by tt.user_id) as t right outer join SinaVerified.dbo.MiningOri5 as mo5 on t.user_id=mo5.user_id
) as offTime on workTime.user_id=offTime.user_id
inner join SinaVerified.dbo.users_type as ut on workTime.user_id=ut.user_id






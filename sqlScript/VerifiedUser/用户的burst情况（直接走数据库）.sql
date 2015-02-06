
select t.user_id, t.type, 
case when td.burst IS null then 0 else td.burst end as burst,
t.total
from
(
select t.user_id,t.type,COUNT(*)as burst
from SinaVerified.dbo.timeDiff as t
where t.timeDiff<=10
group by t.user_id,t.type

) as td right outer join 
(

select td.user_id,td.type,COUNT(*) as total
from SinaVerified.dbo.timeDiff as td
group by td.user_id,td.type
) as t on td.user_id=t.user_id 

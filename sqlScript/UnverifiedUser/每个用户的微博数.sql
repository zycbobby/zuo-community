select s.user_id, COUNT(*)
from SinaUnverified.dbo.status as s
group by s.user_id
--having COUNT(*)<180
order by COUNT(*)

go


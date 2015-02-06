
select s.user_id, COUNT(s.status_id)
from SinaVerified.dbo.status as s
where s.status_id>3415643573514472
group by s.user_id
having COUNT(s.status_id)>0
order by COUNT(*) desc
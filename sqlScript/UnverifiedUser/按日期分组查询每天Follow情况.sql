

select convert(varchar(10),ur.update_time,111) as Update_Time,ur.target_user_id,SUM(ur.follow) as fCount
from SinaUnVerified.dbo.user_relation as ur
where ur.update_time>'2012-1-18'
group by convert(varchar(10),ur.update_time,111),ur.target_user_id
having SUM(ur.follow)>200
order by convert(varchar(10),ur.update_time,111) asc

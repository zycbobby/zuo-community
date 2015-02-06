--其实就是确认一下，哪一天开始的数据是比较准确的

select convert(varchar(10),ur.update_time,111) as Update_Time,SUM(follow) as  fCount,SUM(unfollow) as ufCount
from SinaVerified.dbo.user_relation as ur
group by convert(varchar(10),ur.update_time,111)
order by convert(varchar(10),ur.update_time,111) asc

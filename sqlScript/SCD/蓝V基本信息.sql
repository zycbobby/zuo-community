
select t.*,COUNT(s.status_id) as rtCount
from 
(

select u.user_id,u.screen_name,u.followers_count,COUNT(s.status_id) as stastusMonth, SUM(rc.rtCount) as rtCount,SUM(rc.cmtCount) as cmtCount
from SinaVerified.dbo.users as u
inner join SinaVerified.dbo.users_type as ut 
on u.user_id=ut.user_id and ut.type=1

inner join SinaVerified.dbo.status as s 
on u.user_id=s.user_id

inner join SinaVerified.dbo.rt_cmt as rc
on s.status_id=rc.status_id 

group by u.user_id,u.screen_name,u.followers_count) as t inner join
SinaVerified.dbo.status as s
on t.user_id=s.user_id and s.retweeted_status_id is not null
group by t.user_id,t.screen_name,t.followers_count,t.stastusMonth,t.rtCount,t.cmtCount
order by t.user_id asc
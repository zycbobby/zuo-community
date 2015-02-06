select top 500 s.content, s.created_at,s.original_pic,u.screen_name,rc.cmtCount,rc.rtCount 
from SinaVerified.dbo.status as s
inner join 
SinaVerified.dbo.users as u on s.user_id=u.user_id
inner join
SinaVerified.dbo.users_type as ut on u.user_id=ut.user_id
inner join SinaVerified.dbo.rt_cmt as rc on s.status_id=rc.status_id
where s.retweeted_status_id is null and ut.type=1
order by rc.cmtCount+rc.rtCount desc
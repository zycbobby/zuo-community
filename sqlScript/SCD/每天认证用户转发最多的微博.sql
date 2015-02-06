
select convert(varchar(10),s.created_at,111), t.rtCount,s.status_id,s.content,s.created_at, s.source_name,s.original_pic, u.user_id,u.screen_name
from 
(
select rc.*
from SinaUnverified.dbo.status_rt_cmt_verified_all as rc
inner join SinaUnverified.dbo.status_mix_verified as s on rc.status_id=s.status_id
where rc.rtCount>10000
) as t
inner join SinaUnverified.dbo.status_mix_verified as s
on t.status_id=s.status_id
inner join SinaUnverified.dbo.users as u on s.user_id=u.user_id
order by s.status_id asc, t.rtCount desc

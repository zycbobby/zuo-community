select top 100 s.*,u.screen_name,rc.retweet_count
from SinaUnverified.dbo.status_rt_cmt_verified as rc
inner join
SinaUnverified.dbo.status_mix_verified as s
on rc.status_id=s.status_id
inner join
SinaVerified.dbo.users as u
on s.user_id=u.user_id
where u.verified_type=0
order by rc.retweet_count desc

go
select top 100 s.*,u.screen_name,rc.comment_count
from SinaUnverified.dbo.status_rt_cmt_verified as rc
inner join
SinaUnverified.dbo.status_mix_verified as s
on rc.status_id=s.status_id
inner join
SinaUnverified.dbo.users as u
on s.user_id=u.user_id
order by rc.comment_count desc
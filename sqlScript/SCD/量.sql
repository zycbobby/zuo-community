

select SUM(rc.retweet_count)
from SinaUnverified.dbo.status_rt_cmt as rc
--where rc.retweet_count=0


select *
from SinaUnverified.dbo.status as  s
where s.status_id=3350733374983436

select COUNT(*)
from SinaUnverified.dbo.status_rt_cmt_verified as rc
where status_id<3350733374983436

select SUM(rc.retweet_count)
from SinaUnverified.dbo.status_rt_cmt_verified as rc
where status_id<3350733374983436
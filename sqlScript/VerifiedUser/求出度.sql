declare @utype int
declare @leastOriTweet int
set @utype=1
set @leastOriTweet=5

select u.user_id,uall.screen_name, u.type,COUNT(*)
from SinaVerified.dbo.user_relation_c as ur
inner join 
SinaVerified.dbo.users_type as  u on ur.source_user_id=u.user_id
inner join
SinaVerified.dbo.users as  uall on ur.source_user_id=uall.user_id
--inner join
--SinaVerified.dbo.originalTweetCount as otc on ur.target_user_id=otc.user_id
--where otc.oriTweetCnt>=@leastOriTweet
group by u.user_id,uall.screen_name, u.type
order by COUNT(*) desc
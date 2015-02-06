declare @utype int
declare @leastOriTweet int
set @utype=1
set @leastOriTweet=5

if OBJECT_ID('tempdb..##indegree') is not null
drop table tempdb..##indegree

if OBJECT_ID('tempdb..##outdegree') is not null
drop table tempdb..##outdegree

select u.user_id,uall.screen_name, u.type,COUNT(*) as inCount
into ##indegree
from SinaVerified.dbo.user_relation_c as ur
inner join 
SinaVerified.dbo.users_type as  u on ur.target_user_id=u.user_id
inner join
SinaVerified.dbo.users as  uall on ur.target_user_id=uall.user_id
--inner join
--SinaVerified.dbo.originalTweetCount as otc on ur.target_user_id=otc.user_id
--where otc.oriTweetCnt>=@leastOriTweet
group by u.user_id,uall.screen_name, u.type
order by COUNT(*) desc
select * from ##indegree


select u.user_id,uall.screen_name, u.type,COUNT(*) as outCount
into ##outdegree
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


select idg.user_id, idg.inCount+odg.outCount
from ##indegree as idg inner join ##outdegree as odg on idg.user_id=odg.user_id

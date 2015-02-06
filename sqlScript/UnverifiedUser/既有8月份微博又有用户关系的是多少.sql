select COUNT(*)
from SinaUnverified.dbo.users_being_crawled as uwithT,
(  select user_id
  from SinaUnVerified.dbo.users
  where verified=0 and followers_count>100 and friends_count>30 and friends_count<1000) as uwithR
  where uwithT.user_id=uwithR.user_id
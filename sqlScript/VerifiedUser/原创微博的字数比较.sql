select s.user_id,CAST(AVG(LEN(s.content)) as float), uType.type
from SinaVerified.dbo.status as s
inner join 
SinaVerified.dbo.originalTweetCount as ori on s.user_id=ori.user_id
right join
SinaVerified.dbo.users_type as uType on s.user_id=uType.user_id
where ori.oriTweetCnt>5
group by s.user_id,uType.type
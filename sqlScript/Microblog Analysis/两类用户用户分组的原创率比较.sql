--先找出机构用户发的所有微博

declare @usertype int
set @usertype=2


select COUNT(*) as allTweetsCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype

--转发微博
select COUNT(*) as retweetCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and s.retweeted_status_id is not null

--有脸的机构发的所有微博
select COUNT(*) as rtCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and su.facecount>0


--有脸的机构发的所有转发微博
select COUNT(*) as retweetCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and su.facecount>0 and s.retweeted_status_id is not null





--���ҳ������û���������΢��

declare @usertype int
set @usertype=2


select COUNT(*) as allTweetsCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype

--ת��΢��
select COUNT(*) as retweetCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and s.retweeted_status_id is not null

--�����Ļ�����������΢��
select COUNT(*) as rtCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and su.facecount>0


--�����Ļ�����������ת��΢��
select COUNT(*) as retweetCount
from SinaVerified.dbo.status as s,
SinaVerified.dbo.sample_users as su
where su.user_id=s.user_id and su.usertype=@usertype and su.facecount>0 and s.retweeted_status_id is not null





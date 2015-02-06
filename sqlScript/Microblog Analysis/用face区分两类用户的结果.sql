

select cast(SUM(facecount) as float)/CAST(COUNT(*) as float)
from SinaVerified.dbo.sample_users as su
where su.usertype=2


select *
from SinaVerified.dbo.sample_users as su
where su.usertype=2 and su.facecount>0


select *
from SinaVerified.dbo.sample_users as su
where su.usertype=1 and su.facecount=0

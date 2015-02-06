

declare @singleuser int
declare @groupuser int

set @singleuser=
(select COUNT(*)
from SinaVerified.dbo.sample_users
where usertype=1)


set @groupuser=
(select COUNT(*) from SinaVerified.dbo.sample_users where usertype=2)

print @singleuser
print @groupuser


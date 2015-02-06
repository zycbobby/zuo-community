select COUNT(*)
from SinaVerified.dbo.users
where verified_type>=0 and verified_type<=7

go

select COUNT(*)
from SinaVerified.dbo.users
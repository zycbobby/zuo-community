select COUNT(*)
from SinaUnverified.dbo.users  as u
where u.verified=0

select COUNT(*)
from SinaUnverified.dbo.users  as u
inner join
SinaUnverified.dbo.status as s
on u.user_id=s.user_id
where u.verified=0

go

select COUNT(*)
from SinaVerified.dbo.users_type

select COUNT(*)
from SinaVerified.dbo.users  as u
inner join
SinaVerified.dbo.status as s
on u.user_id=s.user_id
go

select COUNT(*)
from SinaVerified.dbo.users_type as ut
where ut.type>0

select COUNT(*)
from SinaVerified.dbo.users_type as ut
inner join
SinaVerified.dbo.status as s
on ut.user_id=s.user_id
where ut.type>0
go
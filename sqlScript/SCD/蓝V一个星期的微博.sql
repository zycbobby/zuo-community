
declare @sid1 bigint
set @sid1=3348617123060945

--8.26最大的微博
declare @sid2 bigint
set @sid2=3350791449387560

--用于算运行了百分之几的
declare @sid3 bigint
set @sid3=3349565056918593
/*
select COUNT(*)
from SinaVerified.dbo.status as s inner join SinaVerified.dbo.users_type as ut on s.user_id=ut.user_id and ut.type=1
where s.status_id>@sid1 and s.status_id<@sid3
*/



select s.status_id
from SinaVerified.dbo.status as s inner join SinaVerified.dbo.users_type as ut on s.user_id=ut.user_id and ut.type=1
where s.status_id>@sid2

order by s.status_id





/*要用202那个机器的数据库才可以，不过那个数据库的关系是2012.2.15 开始的*/
/*select COUNT(user_id)
from SinaVerified.dbo.users

select COUNT(status_id)
from SinaVerified.dbo.status*/

select COUNT(*)
from SinaVerified.dbo.user_relation


go

/*
use SinaUnverified
select COUNT(user_id)
from SinaUnverified.dbo.users
where verified=0

select COUNT(status_id)
from SinaUnverified.dbo.status

select SUM(ur.follow)-SUM(unfollow)
from SinaUnverified.dbo.user_relation as ur
inner join SinaUnverified.dbo.users as u1 on ur.source_user_id=u1.user_id
inner join SinaUnverified.dbo.users as u2 on ur.target_user_id=u2.user_id
go
*/
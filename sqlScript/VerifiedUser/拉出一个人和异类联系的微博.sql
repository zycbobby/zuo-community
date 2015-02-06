declare @uid bigint
set @uid=1033102464

select u.*,s.*
from SinaVerified.dbo.users as u
inner join
SinaVerified.dbo.status as s
on u.user_id=s.user_id
inner join
SinaVerified.dbo.source_url_with_clientbit as url
on s.status_id=url.status_id
where u.user_id=@uid and url.clientbit=1


--uid AT异类的情况
select u.screen_name,s.*
from SinaVerified.dbo.at_relation as ar
inner join 
SinaVerified.dbo.status as s
on ar.status_id=s.status_id
inner join
SinaVerified.dbo.users_type as ut1
on ut1.user_id=ar.source_user_id
inner join
SinaVerified.dbo.users_type as ut2
on ut2.user_id=ar.target_user_id
inner join
SinaVerified.dbo.users as u
on s.user_id=u.user_id
inner join
SinaVerified.dbo.source_url_with_clientbit as url
on s.status_id=url.status_id
where ar.source_user_id=@uid and ut1.type!=ut2.type and url.clientbit=1


--uid 被异类AT的情况
select u.screen_name,s.*
from SinaVerified.dbo.at_relation as ar
inner join 
SinaVerified.dbo.status as s
on ar.status_id=s.status_id
inner join
SinaVerified.dbo.users_type as ut1
on ut1.user_id=ar.target_user_id
inner join
SinaVerified.dbo.users_type as ut2
on ut2.user_id=ar.source_user_id
inner join
SinaVerified.dbo.users as u
on s.user_id=u.user_id
inner join
SinaVerified.dbo.source_url_with_clientbit as url
on s.status_id=url.status_id
where ar.target_user_id=@uid and ut1.type!=ut2.type and url.clientbit=1

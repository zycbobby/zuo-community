use SinaVerified
declare @crt int
set @crt=1

select at1.target_user_id,at2.target_user_id,ut1.type type1,ut2.type as types2,u1.screen_name,u2.screen_name,COUNT(*) as coorcurance
from at_relation as at1
inner join  
at_relation as at2
on at1.status_id=at2.status_id and at1.target_user_id<at2.target_user_id
inner join users_type as ut1 on ut1.user_id=at1.target_user_id
inner join users_type as ut2 on ut2.user_id=at2.target_user_id
inner join users as u1 on ut1.user_id=u1.user_id
inner join users as u2 on ut2.user_id=u2.user_id
inner join
SinaVerified.dbo.source_url_with_clientbit as url
on at1.status_id=url.status_id
where 
ut1.type!=ut2.type and 
url.clientbit=1
group by at1.target_user_id,at2.target_user_id,ut1.type,ut2.type,u1.screen_name,u2.screen_name
having COUNT(*)>@crt
order by COUNT(*) desc
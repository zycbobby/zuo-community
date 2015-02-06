select COUNT(*)
from SinaVerified.dbo.at_relation as ar
inner join
SinaVerified.dbo.source_url_with_clientbit as s
on ar.status_id=s.status_id
where s.clientbit=1
--这个迟早都是要处理的，原创内容要是weibo.com作为前缀的，用存储过程处理

go

select ar.target_user_id,u.screen_name,count(*)
from SinaVerified.dbo.at_relation as ar
inner join
SinaVerified.dbo.source_url_with_clientbit as s
on ar.status_id=s.status_id
inner join
SinaVerified.dbo.users_type as ut1
on ar.source_user_id=ut1.user_id
inner join
SinaVerified.dbo.users_type as ut2
on ar.target_user_id=ut2.user_id
inner join
SinaVerified.dbo.users as u
on ut2.user_id=u.user_id
and s.clientbit=1
where ut1.type=0 and ut2.type=1  

group by ar.target_user_id,u.screen_name
order by COUNT(*) desc

go
select ar.target_user_id,u.screen_name,COUNT(*)
from SinaVerified.dbo.at_relation as ar
inner join
SinaVerified.dbo.source_url_with_clientbit as s
on ar.status_id=s.status_id
inner join 
SinaVerified.dbo.users_type as ut1
on ar.source_user_id=ut1.user_id
inner join
SinaVerified.dbo.users_type as ut2
on ar.target_user_id=ut2.user_id
inner join
SinaVerified.dbo.users as u
on ut2.user_id=u.user_id
where ut1.type=1 and ut2.type=0
and s.clientbit=1
group by ar.target_user_id,u.screen_name
order by COUNT(*) desc
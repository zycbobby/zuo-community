
select p.source_name, p.pClient,o.oClient
from (

select s.source_name,COUNT(*) as pClient
from SinaVerified.dbo.status as s
inner join SinaVerified.dbo.users_type as ut on s.user_id=ut.user_id
where ut.type=0
group by s.source_name

) as p
inner join
(
select s.source_name,COUNT(*) as oClient
from SinaVerified.dbo.status as s
inner join SinaVerified.dbo.users_type as ut on s.user_id=ut.user_id
where ut.type=1
group by s.source_name

) as o on p.source_name=o.source_name

order by o.oClient desc

--提取小时 from created_at
select s.user_id,ut.type, DATEPART(HH,s.created_at),COUNT(*)
from SinaVerified.dbo.status as s inner join SinaVerified.dbo.users_type as ut on s.user_id=ut.user_id
inner join SinaVerified.dbo.source_url_with_clientbit as sc on s.status_id=sc.status_id
where sc.clientbit=1
group by s.user_id, DATEPART(HH,s.created_at),ut.type
order by user_id,DATEPART(HH,s.created_at)
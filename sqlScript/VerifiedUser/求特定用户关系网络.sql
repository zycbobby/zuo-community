

declare @uid bigint
set @uid=1576193572

if OBJECT_ID('tempdb..##ids') is not null
begin
	drop table ##ids;
end
select un.user_id,ut.type
into ##ids
from (
select ur.target_user_id as user_id
from SinaVerified.dbo.user_relation as ur
where ur.source_user_id=@uid 
union 
select ur.source_user_id as user_id
from SinaVerified.dbo.user_relation as ur
where ur.target_user_id=@uid 
union
select @uid
) as un inner join SinaVerified.dbo.users_type as ut on un.user_id=ut.user_id



select * from ##ids 

select ur.source_user_id,ur.target_user_id
from SinaVerified.dbo.user_relation as ur
where ur.source_user_id in (select user_id from ##ids)
and
ur.target_user_id in (select user_id from ##ids)



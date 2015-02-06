use SinaVerified
declare @uid bigint
set @uid=1808273553

select ar.target_user_id,ut.type, COUNT(*)
from dbo.at_relation as ar
inner join dbo.users_type as ut on ar.target_user_id=ut.user_id
where ar.source_user_id=@uid
group by ar.target_user_id,ut.type

select ar.source_user_id,ut.type, COUNT(*)
from dbo.at_relation as ar
inner join dbo.users_type as ut on ar.source_user_id=ut.user_id
where ar.target_user_id=@uid
group by ar.source_user_id,ut.type
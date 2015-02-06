use SinaVerified
declare @uid1 bigint
declare @uid2 bigint
set @uid1=1721131891
set @uid2=1858313144

select ar1.status_id, ar1.target_user_id,ar2.target_user_id
from at_relation as ar1,
at_relation as ar2
where ar1.target_user_id=@uid1 and ar2.target_user_id=@uid2 and 
ar1.status_id=ar2.status_id
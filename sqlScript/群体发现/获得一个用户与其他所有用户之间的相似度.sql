declare @uid bigint

set @uid=104881;


with list as (
select us.uid2 as user_id, us.h2_sim
from SinaVerified.dbo.user_sim as us
where us.uid1=@uid

union

select @uid as user_id, 0 as h2_sim

union

select us.uid1 as user_id, us.h2_sim
from SinaVerified.dbo.user_sim as us
where us.uid2=@uid)

select *
from list as l
order by l.user_id 
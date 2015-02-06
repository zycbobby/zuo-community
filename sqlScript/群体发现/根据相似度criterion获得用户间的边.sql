declare @sim float

set @sim=0

select us.uid1,us.uid2,us.h2_sim
from SinaVerified.dbo.user_sim as us
where us.h2_sim>@sim
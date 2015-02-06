select ar.status_id,STDEV(CAST(ut.type as float))
from SinaVerified.dbo.at_relation as ar
inner join
SinaVerified.dbo.users_type as ut
on ar.target_user_id=ut.user_id
group by ar.status_id
having COUNT(*)>1
order by STDEV(CAST(ut.type as float)) desc
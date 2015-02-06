select su.*,u.location,u.province,u.city
from SinaVerified.dbo.sample_users as su,
SinaVerified.dbo.users as u
where su.user_id=u.user_id and (su.usertype=1 or su.usertype=2)
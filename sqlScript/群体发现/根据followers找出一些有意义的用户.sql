select *
from SinaVerified.dbo.users as u
where u.verified_type>0 and u.verified_type<8 and followers_count>1000
order by  u.followers_count desc
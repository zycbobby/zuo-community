select valuableUser.verified_type, COUNT(*)
from (select u.*
from SinaVerified.dbo.users as u inner join (SELECT s.user_id, COUNT(*) as twCount
  FROM SinaVerified.dbo.status as s
  group by s.user_id
  having  COUNT(*)>=5) as temp on  u.user_id=temp.user_id
  where u.verified_type>=0 and u.verified_type<10) as valuableUser
  group by valuableUser.verified_type
  order by valuableUser.verified_type 
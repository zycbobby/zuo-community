use SinaVerified
select TOP 2000 *
from status as s inner join users as u on s.user_id=u.user_id
where u.verified_type=0 and s.retweeted_status_id is null and charindex('ÉÏº£',s.content)>0


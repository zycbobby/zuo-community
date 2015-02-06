select uri.source_user_id,uri.target_user_id, COUNT(*),SUM(follow) as followCount,SUM(unfollow) as unfollowCount
from SinaUnVerified.dbo.user_relation_inc as uri
group by uri.source_user_id,uri.target_user_id
order by COUNT(*) desc
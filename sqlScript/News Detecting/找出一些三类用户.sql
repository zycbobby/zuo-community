--这些用户应该是某些用户的双向关系
--而且是没有verified
use sinawler

select distinct u.screen_name,u.description,3,u.followers_count,u.friends_count,u.statuses_count,DATEDIFF(S,u.created_at,u.update_time) as timeConsumed
from dbo.users as u,
(select ur1.target_user_id
from 
(select Top 1000 *
from sinawler.dbo.users as u
where u.verified=0) as testSetUser,
dbo.user_relation as  ur1, dbo.user_relation as ur2 
where ur1.source_user_id=testSetUser.user_id and  ur1.source_user_id=ur2.target_user_id and ur1.target_user_id=ur2.source_user_id) as thirdQUser
where thirdQUser.target_user_id=u.user_id and u.friends_count<1000


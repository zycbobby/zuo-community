select u.user_id, u.user_name,ugc.group_id
from user_group_clustered as ugc inner join users as u
on ugc.user_id=u.user_id
order by u.user_id

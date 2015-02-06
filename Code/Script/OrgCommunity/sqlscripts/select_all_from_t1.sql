select u.user_name, ugc.group_id
from user_group_clustered as ugc
inner join users as u
on u.user_id=ugc.user_id
order by ugc.group_id
select ugc.group_id, count(ugc.user_id) as group_count
from user_group_clustered as ugc
group by ugc.group_id


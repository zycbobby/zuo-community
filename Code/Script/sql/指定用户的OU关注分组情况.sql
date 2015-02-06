select eur.source_user_id, eur.target_user_id,u.user_name,ugc.group_id
from eva_user_relation as eur
inner join users as u on eur.target_user_id=u.user_id
inner join user_group_clustered as ugc on u.user_id=ugc.user_id
where eur.source_user_id=1156966391
order by ugc.group_id

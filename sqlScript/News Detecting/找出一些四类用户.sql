select u.screen_name,u.description,4,u.followers_count,u.friends_count,u.statuses_count,DATEDIFF(S,u.created_at,u.update_time) as timeConsumed
from sinawler.dbo.users as u
where (CHARINDEX('����',u.screen_name)>0 or CHARINDEX('��¼',u.screen_name)>0 or CHARINDEX('ʷ��',u.screen_name)>0 or CHARINDEX('����',u.screen_name)>0 or CHARINDEX('Ц��',u.screen_name)>0 or CHARINDEX('��Ů',u.screen_name)>0) and LEN(u.description)>0 and u.friends_count<1000
and u.verified=0



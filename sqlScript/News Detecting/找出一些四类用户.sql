select u.screen_name,u.description,4,u.followers_count,u.friends_count,u.statuses_count,DATEDIFF(S,u.created_at,u.update_time) as timeConsumed
from sinawler.dbo.users as u
where (CHARINDEX('经典',u.screen_name)>0 or CHARINDEX('语录',u.screen_name)>0 or CHARINDEX('史上',u.screen_name)>0 or CHARINDEX('星座',u.screen_name)>0 or CHARINDEX('笑话',u.screen_name)>0 or CHARINDEX('美女',u.screen_name)>0) and LEN(u.description)>0 and u.friends_count<1000
and u.verified=0



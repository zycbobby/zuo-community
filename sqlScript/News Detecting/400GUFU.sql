

select u.*

from sinawler.dbo.users as u
where (CHARINDEX('����',u.screen_name)>0 or CHARINDEX('��¼',u.screen_name)>0 or CHARINDEX('ʷ��',u.screen_name)>0 or CHARINDEX('����',u.screen_name)>0 or CHARINDEX('Ц��',u.screen_name)>0 or CHARINDEX('��Ů',u.screen_name)>0) and LEN(u.description)>0 and u.friends_count<1000
and u.verified=0

union

select distinct u.*
from dbo.users as u,
(select ur1.target_user_id
from 
(select Top 1000 *
from sinawler.dbo.users as u
where u.verified=0) as testSetUser,
sinawler.dbo.user_relation as  ur1, dbo.user_relation as ur2 
where ur1.source_user_id=testSetUser.user_id and  ur1.source_user_id=ur2.target_user_id and ur1.target_user_id=ur2.source_user_id) as thirdQUser
where thirdQUser.target_user_id=u.user_id and u.friends_count<1000
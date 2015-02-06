--找出source 和target都在我的user库当中的关系
--以18号为标准
declare @groupno int
set @groupno=3
--select ur.source_user_id,ur.target_user_id
--select u1.user_id,u2.user_id

select u1.user_id,u2.user_id,un1.user_no,un2.user_no

from SinaUnVerified.dbo.user_relation as ur,
SinaUnVerified.dbo.users as u1,
SinaUnVerified.dbo.users as u2,
(select ROW_NUMBER() over (order by un.user_id) as user_no,un.user_id
from SinaUnVerified.dbo.UserNo as un
where un.group_no=@groupno
) as un1,
(select ROW_NUMBER() over (order by un.user_id) as user_no,un.user_id
from SinaUnVerified.dbo.UserNo as un
where un.group_no=@groupno
) as un2

where ur.source_user_id=u1.user_id and ur.target_user_id=u2.user_id
and u1.user_id=un1.user_id
and u2.user_id=un2.user_id

group by u1.user_id,u2.user_id,un1.user_no,un2.user_no

having SUM(follow)-SUM(unfollow)>0
--�������ڴʻ����ͷ�ж��ٸ��û��ĵ���

select distinct u.*
from SinaVerified.dbo.status_noun as sn inner join SinaVerified.dbo.status as s
on sn.status_id=s.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id
order by u.followers_count desc

declare @uid bigint
--������
--set @uid=1195403385

--�����--really interesting
--set @uid=2106855375

--��ǫ
--set @uid=1271542887

--����NBAפ��ʢ�����ɼ�������
--set @uid=1822851445

--����
--set @uid=1191258123

--����
--set @uid=1746274673

--����
--set @uid=1759228037

--��������˵�����������֮�����᲻�����йص��أ�

--���ݷ�
set @uid=2424084591

select convert(varchar(10),ur.update_time,111),SUM(ur.follow),SUM(ur.unfollow)
from SinaUnVerified.dbo.user_relation as ur
where ur.target_user_id=@uid and ur.update_time>'2012-1-18'
group by convert(varchar(10),ur.update_time,111)
order by convert(varchar(10),ur.update_time,111) asc

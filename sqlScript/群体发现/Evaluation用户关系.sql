--������һЩ�û�����ȥ�����ҵ�community detect������ô��

--��������Ϣ������עʲô�˺�����ʲô���֣���ʵ����������������һ��������Ҫevaluation���û�������һ���������ǹ�עʲôou

--�������ϲ�����Ҫ��������




with evaluation_users as
(
select urc.target_user_id as user_id,u.name
  from SinaUnverified.dbo.user_relation_c as urc
  inner join SinaUnverified.dbo.users as u on urc.target_user_id=u.user_id
  where urc.source_user_id=1438151640
  union
  select 1438151640 as user_id,'Zuozuo'
  union
  
  SELECT top 100 u.user_id, u.name
  FROM [SinaVerified].[dbo].[users] as u
  where u.verified_type=0
  order by u.followers_count desc
)


select eu.user_id as source_user_id,u.user_id as target_user_id
from SinaVerified.dbo.user_relation_c as urc
inner join SinaVerified.dbo.users as u on urc.target_user_id=u.user_id and u.verified_type>0 and u.verified_type<9
inner join evaluation_users as eu on eu.user_id=urc.source_user_id
order by  eu.user_id

select s1.status_id as sid1, s2.status_id as sid2, DATEDIFF(HH,s1.created_at,s2.created_at) as time_diff
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=sc1.status_id
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h1_label_id=sc2.h1_label_id and sc1.h2_label_id=sc2.h2_label_id
and sc1.h3_label_id=sc2.h3_label_id and sc1.h1_label_id>-1 and sc1.h2_label_id>-1 and sc1.h3_label_id>-1
inner join SinaVerified.dbo.status as s2 on s2.status_id=sc2.status_id
where s1.user_id=1647263235 and s2.user_id=1716488301 and s1.status_id<s2.status_id and DATEDIFF(HH,s1.created_at,s2.created_at)<72
order by time_diff asc
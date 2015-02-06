select top 1000 s.status_id,s.content, u.name,cl1.label_name, cl2.label_name,cl3.label_name
from SinaVerified.dbo.status as s
inner join SinaVerified.dbo.status_cls as sc on s.status_id=sc.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id
left outer join SinaVerified.dbo.cls_label as cl1 on sc.h1_label_id=cl1.label_id
left outer join SinaVerified.dbo.cls_label as cl2 on sc.h2_label_id=cl2.label_id
left outer join SinaVerified.dbo.cls_label as cl3 on sc.h3_label_id=cl3.label_id
select s.content, cl1.label_name,cl2.label_name,cl3.label_name, sc.rank,sc.confidence
from SinaVerified.dbo.status as s
inner join SinaVerified.dbo.status_cls as sc on s.status_id=sc.status_id
left outer join SinaVerified.dbo.cls_label as cl1 on sc.h1_label_id=cl1.label_id
left outer join SinaVerified.dbo.cls_label as cl2 on sc.h2_label_id=cl2.label_id
left outer join SinaVerified.dbo.cls_label as cl3 on sc.h3_label_id=cl3.label_id
where s.user_id=1056089070
order by sc.h1_label_id
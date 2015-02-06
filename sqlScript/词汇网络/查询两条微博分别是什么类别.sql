
declare @sid1 bigint
declare @sid2 bigint

set @sid1=3349132279077328;
set @sid2=3352134964534106;

select s1.content,cl1.label_name,cl1.label_id,cl2.label_id,cl3.label_id,
cl1.label_name,cl2.label_name,cl3.label_name,sc1.rank,sc1.confidence
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=@sid1 and s1.status_id=sc1.status_id
left outer join SinaVerified.dbo.cls_label as cl1 on sc1.h1_label_id=cl1.label_id
left outer join SinaVerified.dbo.cls_label as cl2 on sc1.h2_label_id=cl2.label_id
left outer join SinaVerified.dbo.cls_label as cl3 on sc1.h3_label_id=cl3.label_id

select s1.content,cl1.label_name,cl1.label_id,cl2.label_id,cl3.label_id,
cl1.label_name,cl2.label_name,cl3.label_name,sc1.rank,sc1.confidence
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=@sid2 and s1.status_id=sc1.status_id
left outer join SinaVerified.dbo.cls_label as cl1 on sc1.h1_label_id=cl1.label_id
left outer join SinaVerified.dbo.cls_label as cl2 on sc1.h2_label_id=cl2.label_id
left outer join SinaVerified.dbo.cls_label as cl3 on sc1.h3_label_id=cl3.label_id
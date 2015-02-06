declare @uid bigint
set @uid=1926909715;

with label_t as
(select s.user_id, sc.h1_label_id as label_id, COUNT(*) as label_count
from SinaVerified.dbo.status_cls as sc
inner join SinaVerified.dbo.status as s on sc.status_id=s.status_id
where s.user_id=@uid and sc.h1_label_id<>-1
group by s.user_id,sc.h1_label_id

union


select s.user_id, sc.h2_label_id as label_id, COUNT(*) as label_count
from SinaVerified.dbo.status_cls as sc
inner join SinaVerified.dbo.status as s on sc.status_id=s.status_id
where s.user_id=@uid and sc.h2_label_id<>-1
group by s.user_id,sc.h2_label_id

union

select s.user_id, sc.h3_label_id as label_id, COUNT(*) as label_count
from SinaVerified.dbo.status_cls as sc
inner join SinaVerified.dbo.status as s on sc.status_id=s.status_id
where s.user_id=@uid and sc.h3_label_id<>-1
group by s.user_id,sc.h3_label_id)


select * from label_t as lt order by lt.user_id, lt.label_id
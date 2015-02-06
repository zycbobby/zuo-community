
if OBJECT_ID('tempdb..##puvalue') is not null
drop table tempdb..##puvalue

if OBJECT_ID('tempdb..##ouvalue') is not null
drop table tempdb..##ouvalue

if OBJECT_ID('tempdb..##pfvalue') is not null
drop table tempdb..##pfvalue

if OBJECT_ID('tempdb..##ofvalue') is not null
drop table tempdb..##ofvalue

if object_id('tempdb..##cooccur') is not null
drop table tempdb..##cooccur

go
use SinaVerified

select at1.target_user_id as uid1, at2.target_user_id as uid2, count(*) as coTime
into ##cooccur
from dbo.at_relation as at1 inner join dbo.at_relation as at2
on at1.status_id=at2.status_id and at1.target_user_id!=at2.target_user_id
group by at1.target_user_id , at2.target_user_id

--select * from ##cooccur

select p.user_id, case when t.puv is null then 0 else t.puv end as puv, 
case when t.puc is null then 0 else t.puc end as puc
into ##puvalue
from (
select p1.user_id, SUM(p2.probability) as puv, count(*) as puc

from dbo.predict as p1
left outer join ##cooccur as co on p1.user_id=co.uid1,
dbo.predict as p2 
where p2.ptype=0 and p2.user_id=co.uid2
group by p1.user_id) 
as t right outer join dbo.predict as p on t.user_id=p.user_id



select p.user_id, case when t.ouv is null then 0 else t.ouv end as ouv, 
case when t.ouc is null then 0 else t.ouc end as ouc
into ##ouvalue
from (
select p1.user_id, SUM(p2.probability) as ouv, count(*) as ouc
from dbo.predict as p1
left outer join ##cooccur as co on p1.user_id=co.uid1,
dbo.predict as p2 
where p2.ptype=1 and p2.user_id=co.uid2
group by p1.user_id) as t right outer join dbo.predict as p on t.user_id=p.user_id


select p.user_id, case when t.pfv is null then 0 else t.pfv end as pfv, 
case when t.pfc is null then 0 else t.pfc end as pfc
into ##pfvalue
from (
select p1.user_id, SUM(p2.probability) as pfv, count(*) as pfc
from dbo.predict as p1
left outer join dbo.bi_relation as ur on p1.user_id=ur.source_user_id,
dbo.predict as p2 
where p2.ptype=0 and p2.user_id=ur.target_user_id
group by p1.user_id) 
as t right outer join dbo.predict as p on t.user_id=p.user_id


select p.user_id, case when t.ofv is null then 0 else t.ofv end as ofv, 
case when t.ofc is null then 0 else t.ofc end as ofc
into ##ofvalue
from (
select p1.user_id, SUM(p2.probability) as ofv, count(*) as ofc
from dbo.predict as p1
left outer join dbo.bi_relation as ur on p1.user_id=ur.source_user_id,
dbo.predict as p2 
where p2.ptype=1 and p2.user_id=ur.target_user_id
group by p1.user_id) 
as t right outer join dbo.predict as p on t.user_id=p.user_id


select p.*, pv.puv, ov.ouv ,pv.puc, ov.ouc,pfv.pfv, ofv.ofv, pfv.pfc, ofv.ofc,
case when ft.total IS null then 0 else ft.total end as total,
case when ft.figureType IS null then 0 else ft.figureType end as figureType
from ##puvalue as pv inner  join ##ouvalue as ov on pv.user_id=ov.user_id
inner join dbo.predict as p on p.user_id=pv.user_id
inner join ##pfvalue as pfv on pv.user_id=pfv.user_id
inner join ##ofvalue as ofv on pv.user_id=ofv.user_id
left outer join SinaVerified.dbo.figureType as ft on p.user_id=ft.uid

--where (pv.puc!=0 or ov.ouc!=0 )
order by p.user_id
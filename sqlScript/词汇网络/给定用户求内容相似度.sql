/*
给定两个用户id，然后分别求他们的微博有多少仅在一级相同，有多少仅在2级相同，有多少在3级都相同
并且算出这两条微博的时间差
*/

declare @id1 bigint
declare @id2 bigint

set @id1=1647263235;
set @id2=1716488301;

/**分别有多少条原创微博*/
select COUNT(*) from SinaVerified.dbo.status as s where s.user_id=@id1 and s.retweeted_status_id is null;
select COUNT(*) from SinaVerified.dbo.status as s where s.user_id=@id2 and s.retweeted_status_id is null;


/**在三级都相同的*/
/*在两级别相同*/
/**在一级别相同*/
with tri_same as(
select s1.status_id as sid1, s2.status_id as sid2,s1.content as content1, s2.content as content2, sc1.h1_label_id,DATEDIFF(HH,s1.created_at,s2.created_at) as time_diff,cl1.label_name as l1_name,cl2.label_name as l2_name,cl3.label_name as l3_name
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=sc1.status_id
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h1_label_id=sc2.h1_label_id and sc1.h2_label_id=sc2.h2_label_id
and sc1.h3_label_id=sc2.h3_label_id and sc1.h1_label_id>-1 and sc1.h2_label_id>-1 and sc1.h3_label_id>-1
inner join SinaVerified.dbo.status as s2 on s2.status_id=sc2.status_id
inner join SinaVerified.dbo.cls_label as cl1 on sc1.h1_label_id=cl1.label_id
inner join SinaVerified.dbo.cls_label as cl2 on sc1.h2_label_id=cl2.label_id
inner join SinaVerified.dbo.cls_label as cl3 on sc1.h3_label_id=cl3.label_id
where s1.user_id=@id1 and s2.user_id=@id2 and s1.status_id<s2.status_id
),
double_same as (select s1.status_id as sid1, s2.status_id as sid2,s1.content as content1, s2.content as content2,sc1.h1_label_id,DATEDIFF(HH,s1.created_at,s2.created_at) as time_diff,cl1.label_name as l1_name,cl2.label_name as l2_name
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=sc1.status_id
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h1_label_id=sc2.h1_label_id and sc1.h2_label_id=sc2.h2_label_id
and (sc1.h3_label_id<>sc2.h3_label_id or (sc1.h3_label_id=-1 and sc2.h3_label_id=-1))and sc1.h1_label_id>-1 and sc1.h2_label_id>-1
inner join SinaVerified.dbo.status as s2 on s2.status_id=sc2.status_id
inner join SinaVerified.dbo.cls_label as cl1 on sc1.h1_label_id=cl1.label_id
inner join SinaVerified.dbo.cls_label as cl2 on sc1.h2_label_id=cl2.label_id
where s1.user_id=@id1 and s2.user_id=@id2 and s1.status_id<s2.status_id
),
single_same as (select s1.status_id as sid1, s2.status_id as sid2,s1.content as content1, s2.content as content2,sc1.h1_label_id,DATEDIFF(HH,s1.created_at,s2.created_at) as time_diff,cl1.label_name
from SinaVerified.dbo.status as s1
inner join SinaVerified.dbo.status_cls as sc1 on s1.status_id=sc1.status_id
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h1_label_id=sc2.h1_label_id and (sc1.h2_label_id<>sc2.h2_label_id or (sc1.h2_label_id=-1 and sc2.h2_label_id=-1)) 
inner join SinaVerified.dbo.status as s2 on s2.status_id=sc2.status_id
inner join SinaVerified.dbo.cls_label as cl1 on sc1.h1_label_id=cl1.label_id
where s1.user_id=@id1 and s2.user_id=@id2 and s1.status_id<s2.status_id)

select ts.*
from tri_same as ts where ts.time_diff<72

select ds.*
from double_same as ds where ds.time_diff<72

select ss.*
from single_same as ss where ss.time_diff<72


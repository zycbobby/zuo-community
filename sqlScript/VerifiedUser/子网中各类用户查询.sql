/****** Script for SelectTopNRows command from SSMS  ******/
if OBJECT_ID('tempdb..##pu') is not null
drop table tempdb..##pu

if OBJECT_ID('tempdb..##ou') is not null
drop table tempdb..##ou

go

select top 10000 ut.user_id  into ##pu from SinaVerified.dbo.users_type as ut where ut.type=0 order by NEWID()
select top 10000 ut.user_id  into ##ou from SinaVerified.dbo.users_type as ut where ut.type=1 order by NEWID()

SELECT COUNT(*)
  FROM [SinaVerified].[dbo].[bi_relation] as b1 inner join SinaVerified.dbo.users_type as ut1 on b1.source_user_id=ut1.user_id
  inner join
  SinaVerified.dbo.users_type as ut2 on b1.target_user_id=ut2.user_id
  
  where b1.source_user_id<b1.target_user_id
  and ut1.user_id in (select user_id from ##pu)
  and ut2.user_id in (select user_id from ##pu)
  
  
  SELECT COUNT(*)
  FROM [SinaVerified].[dbo].[bi_relation] as b1 inner join SinaVerified.dbo.users_type as ut1 on b1.source_user_id=ut1.user_id
  inner join
  SinaVerified.dbo.users_type as ut2 on b1.target_user_id=ut2.user_id
  
  where b1.source_user_id<b1.target_user_id
  and ut1.user_id in (select user_id from ##pu)
  and ut2.user_id in (select user_id from ##ou)
  
  SELECT COUNT(*)
  FROM [SinaVerified].[dbo].[bi_relation] as b1 inner join SinaVerified.dbo.users_type as ut1 on b1.source_user_id=ut1.user_id
  inner join
  SinaVerified.dbo.users_type as ut2 on b1.target_user_id=ut2.user_id
  
  where b1.source_user_id<b1.target_user_id
  and ut1.user_id in (select user_id from ##ou)
  and ut2.user_id in (select user_id from ##pu)
  
    SELECT COUNT(*)
  FROM [SinaVerified].[dbo].[bi_relation] as b1 inner join SinaVerified.dbo.users_type as ut1 on b1.source_user_id=ut1.user_id
  inner join
  SinaVerified.dbo.users_type as ut2 on b1.target_user_id=ut2.user_id
  
  where b1.source_user_id<b1.target_user_id
  and ut1.user_id in (select user_id from ##ou)
  and ut2.user_id in (select user_id from ##ou)
  
  --求每个人有多少pbirelation ，有多少obirealtion
  select p.user_id, ut.type, COUNT(*) biCount, SUM(ut2.type) as obiCount
  from ##pu as p inner join SinaVerified.dbo.users_type as ut on p.user_id=ut.user_id
  inner join SinaVerified.dbo.bi_relation as bi on p.user_id=bi.source_user_id
  inner join SinaVerified.dbo.users_type as ut2 on bi.target_user_id=ut2.user_id
  group by p.user_id, ut.type
  
/****** Script for SelectTopNRows command from SSMS  ******/
select u.* 
into sinawler.dbo.sample_users
from 
dbo.users as u,
( SELECT gfu.user_id, COUNT(*) as cnt
  FROM [sinawler].[dbo].[GUFU] as gfu,
  (select * from sinawler.dbo.statuses union select * from sinamicroblog.dbo.statuses)  as s
  where s.user_id=gfu.user_id
  group by gfu.user_id
  having COUNT(*)>5) as tu
  where u.user_id=tu.user_id
  
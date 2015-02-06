/****** Script for SelectTopNRows command from SSMS  ******/
select COUNT(*)
  FROM [SinaUnverified].[dbo].[status]
  
  
  go
SELECT COUNT(*)
  FROM [SinaUnverified].[dbo].[users_being_crawled]
  where iteration=1109
  
  go
  
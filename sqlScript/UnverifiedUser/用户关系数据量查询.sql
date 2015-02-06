/****** Script for SelectTopNRows command from SSMS  ******/

  
 -- select COUNT(*)
  --FROM [SinaUnverified].[dbo].[user_relation]
  
  --go
  --select count(*) 
  --from 
  --(
  --select source_user_id
  --from SinaUnVerified.dbo.[user_relation]
  --group by source_user_id 
  --) as s 
  
  go
  select  COUNT(*)
  from [SinaUnverified].[dbo].[user_relation]
  where update_time>'2012-2-9'
  
  go
  
  --²é´í
  --select source_user_id,target_user_id,SUM(follow)-SUM(unfollow)
  --from [SinaUnverified].[dbo].[user_relation]
  --group by source_user_id,target_user_id
  --having SUM(follow)-SUM(unfollow)>1 or SUM(follow)-SUM(unfollow)<-1
  --order by source_user_id
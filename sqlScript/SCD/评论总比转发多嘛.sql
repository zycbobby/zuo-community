/****** Script for SelectTopNRows command from SSMS  ******/
SELECT COUNT(*) as rtMore
  FROM [SinaUnverified].[dbo].[status_rt_cmt]
  where retweet_count>comment_count
  
  SELECT COUNT(*) as cmMore
  FROM [SinaUnverified].[dbo].[status_rt_cmt]
  where retweet_count<comment_count
  
  SELECT COUNT(*) as equal
  FROM [SinaUnverified].[dbo].[status_rt_cmt]
  where retweet_count=comment_count
 
SELECT COUNT(*) as rtMore
  FROM [SinaUnverified].[dbo].[status_rt_cmt_verified]
  where retweet_count>comment_count
  
  SELECT COUNT(*) as cmMore
  FROM [SinaUnverified].[dbo].[status_rt_cmt_verified]
  where retweet_count<comment_count
  
  SELECT COUNT(*) as equal
  FROM [SinaUnverified].[dbo].[status_rt_cmt_verified]
  where retweet_count=comment_count
/****** Script for SelectTopNRows command from SSMS  ******/

--58W/58W
SELECT COUNT(*)
  FROM [SinaUnverified].[dbo].[status_rt_cmt_verified] as rtv inner join SinaUnverified.dbo.status_mix_verified as s
  on rtv.status_id=s.status_id
  where s.retweeted_status_id is null
  
  
  --110W/61W

  SELECT COUNT(*)
  FROM [SinaUnverified].[dbo].[status_rt_cmt_verified_all] as rtv inner join SinaUnverified.dbo.status_mix_verified as s
  on rtv.status_id=s.status_id
  where s.retweeted_status_id is null
  
  
  
  
  [status_rt_cmt_verified_all] 是认证用户发的原创微薄的转发数，当然也包括非原创微博的转发数
  
  
  status_mix_verified 1W认证用户发的所有微博
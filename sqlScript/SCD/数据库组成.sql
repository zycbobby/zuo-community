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
  
  
  
  
  [status_rt_cmt_verified_all] ����֤�û�����ԭ��΢����ת��������ȻҲ������ԭ��΢����ת����
  
  
  status_mix_verified 1W��֤�û���������΢��
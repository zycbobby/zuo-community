SELECT user_id
  FROM SinaUnVerified.[dbo].[users]
  where verified=0 and statuses_count>5
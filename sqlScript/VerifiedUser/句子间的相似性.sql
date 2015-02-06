select mo5.[user_id]
      ,[avg_content_length]
      ,[mediaCount]
      ,[mePercentage]
      ,[mbCount]
      ,[mbPercentage]
      ,[oriCount]
      ,[oriPercentage]
      ,[tweetCount]
      ,uts.similarity
      ,[user_type]
from SinaVerified.dbo.MiningOri5 as mo5
left outer join 
SinaVerified.dbo.user_tweet_similarity as uts on mo5.user_id=uts.user_id
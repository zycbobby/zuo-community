
/****** Script for SelectTopNRows command from SSMS  ******/
if OBJECT_ID('tempdb..##bi_r') is not null
	drop table tempdb..##bi_r
	
if OBJECT_ID('tempdb..##ttime') is not null
drop table tempdb..##ttime
go

use SinaVerified

select t.id1,t.id2
into ##bi_r
from
(select br.source_user_id as id1,br.target_user_id as id2
from SinaVerified.dbo.bi_relation as br
union
select br.target_user_id as id1,br.source_user_id as id2
from SinaVerified.dbo.bi_relation as br) as t

select s.user_id,Datepart(MONTH,s.created_at) as [month],Datepart(DAY,s.created_at) as [day],DATEPART(WEEKDAY,s.created_at) as [weekday], DATEPART(hh,s.created_at)*60+DATEPART(mi,s.created_at) as minInDay

into ##ttime
from SinaVerified.dbo.status as s 

select t.user_id,t.screen_name,
case when t.avg_behavior is null then 0
else t.avg_behavior end as avg_behavior,
t.avg_content_length,
t.minContentLength,
t.mbCount,
t.mbPercentage,
t.mediaCount,
t.mePercentage,
t.oriCount,
t.oriPercentage,
t.similarity,
t.tweetCount,
t.verifiedFriends,
t.biCount,
t.friends_count,
t.atCnt,
t.atDisCnt,
t.stddevofTime,
t.offRatio,
t.user_type
from (SELECT mo5.user_id,
	u.screen_name
      ,[avg_content_length]
      ,mocl.minContentLength
      ,[mediaCount]
      ,[mePercentage]
      ,[mbCount]
      ,[mbPercentage]
      ,[oriCount]
      ,[oriPercentage]
      ,[tweetCount]
      ,uts.similarity as similarity
      ,behav.behaviorCount as behaviorCount
      ,behav.behaviorDays as behaviorDays
      ,behav.behaviorCount*1.0/(1.0*behav.behaviorDays) as avg_behavior
      ,case when (vfriend.verifiedFriends IS null) then 0
      else vfriend.verifiedFriends end as verifiedFriends
      ,case when vfollow.verifiedFollowers is null then 0
      else vfollow.verifiedFollowers end as verifiedFollowers
      ,
      case when oFriends.oFriendsCount is null then 0
      else oFriends.oFriendsCount end as oFriends
      ,
      
      case when biCount.biCount IS null then 0
      else biCount.biCount end as biCount,
      
      
      case when biCount.obiCount IS null then 0
      else biCount.obiCount end as obiCount,
      
      
      u.friends_count,
      [user_type],
      case when atCount.cnt IS null then 0
      else atCount.cnt end as atCnt,
      case when atDisIdCount.cnt IS null then 0
      else atDisIdCount.cnt end as atDisCnt,
      
      earliestTweetInDay.stddevofTime,
      workDivoff.offRatio
      
  FROM [SinaVerified].[dbo].[MiningOri5] as mo5
   inner join SinaVerified.dbo.user_tweet_similarity as uts
   on mo5.user_id=uts.user_id
   left outer join SinaVerified.dbo.behavior as behav
   on mo5.user_id=behav.user_id
   left outer join
   (select ur.source_user_id,count(*) as verifiedFriends
   from SinaVerified.dbo.user_relation as ur 
   group by ur.source_user_id) as vfriend on mo5.user_id=vfriend.source_user_id
   left outer join
   (select ur.target_user_id,count(*) as verifiedFollowers
   from SinaVerified.dbo.user_relation as ur
   group by ur.target_user_id) as vfollow on mo5.user_id=vfollow.target_user_id
   
   left outer join
   (
   select at.source_user_id as user_id, COUNT(at.status_id)  as cnt
from SinaVerified.dbo.at_relation as at
group by at.source_user_id
   ) as atCount on mo5.user_id=atCount.user_id
   
   left outer join
   (
select ar.source_user_id as user_id,COUNT(distinct ar.target_user_id) as cnt
from SinaVerified.dbo.at_relation as ar
group by ar.source_user_id
   ) as atDisIdCount on mo5.user_id=atDisIdCount.user_id
   
   left outer join (
   select ur.source_user_id as user_id,ut2.type, 
case when COUNT(*) is null then 0
else COUNT(*) end as verifiedFriendsCount, SUM(ut.type) as oFriendsCount
from dbo.user_relation as ur left outer join SinaVerified.dbo.users_type as ut on ur.target_user_id=ut.user_id
inner join dbo.users_type as ut2 on ur.source_user_id=ut2.user_id
group by ur.source_user_id,ut2.type
   ) as oFriends on mo5.user_id=oFriends.user_id
   
   left outer join
   (
   select br.id1 as user_id,ut2.type, COUNT(*) as biCount, SUM(ut1.type) as obiCount
from ##bi_r as br inner join dbo.users_type as ut1 on br.id2=ut1.user_id
inner join dbo.users_type as ut2 on br.id1=ut2.user_id
group by br.id1,ut2.type
   ) as biCount on mo5.user_id=biCount.user_id
   
   left outer join 
   SinaVerified.dbo.users as u on mo5.user_id=u.user_id 
   
   inner join
   SinaVerified.dbo.minOriginalContentLength as mocl on mo5.user_id=mocl.user_id
   
   
   left outer join
   (
   select earliestTweetInDay.user_id, STDEV(earliestTweetInDay.eTweetTime) as stddevofTime
from 
(
select t.user_id, min(t.minInDay) as eTweetTime
from (

select s.user_id,Datepart(M,s.created_at) as [month],Datepart(D,s.created_at) as [day],DATEPART(WEEKDAY,s.created_at) as [weekday], DATEPART(hh,s.created_at)*60+DATEPART(mi,s.created_at) as minInDay
from SinaVerified.dbo.status as s 
) as t
group by t.user_id, t.month,t.day

) as earliestTweetInDay right outer join SinaVerified.dbo.MiningOri5  as mo5 on earliestTweetInDay.user_id=mo5.user_id
group  by earliestTweetInDay.user_id
   ) as earliestTweetInDay on mo5.user_id=earliestTweetInDay.user_id
   
   
   left outer join
   (
   select workTime.user_id, offTime.offTimeTweet*1.0/(workTime.workTimeTweet*1.0) as offRatio
from (

--平时的条数，得保证平时有微博才可以，周末可以没有
select mo5.user_id, workTimeTweet
from 
(select tt.user_id,COUNT(*) as workTimeTweet
from ##ttime as tt
where tt.[weekday]>0 and tt.[weekday]<7
group by tt.user_id) as t right outer join SinaVerified.dbo.MiningOri5 as mo5 on t.user_id=mo5.user_id
) as workTime
inner join 
(

--周末的条数
select mo5.user_id, 
case  when t.offTimeTweet is null then 0 else t.offTimeTweet end as offTimeTweet
from 
(select tt.user_id,COUNT(*) as offTimeTweet
from ##ttime as tt
where tt.[weekday]=0 or tt.[weekday]=7
group by tt.user_id) as t right outer join SinaVerified.dbo.MiningOri5 as mo5 on t.user_id=mo5.user_id
) as offTime on workTime.user_id=offTime.user_id
   ) as workDivoff on mo5.user_id=workDivoff.user_id
   
   ) as t
   
   
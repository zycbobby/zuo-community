use SinaVerified
declare @twCountCritierior int
declare @oritwCountCritierior int


set @twCountCritierior=0
set @oritwCountCritierior=0

select avgCL.user_id,avgCL.avgContentLength, mec.mediaCount,CAST(mec.mediaCount as float)/oc.oriTweetCnt as mePercentage,
moc.mobileCount,CAST(moc.mobileCount as float)/utc.twCount as mbPercentage,
oc.oriTweetCnt,CAST(oc.oriTweetCnt as float)/utc.twCount as oriPercentage,
utc.twCount,
ut.type
from 
dbo.users_type as ut 
left outer join
dbo.avgOriginalContentLength as avgCL on ut.user_id=avgCL.user_id
left outer join
dbo.mediaCount as mec on ut.user_id=mec.user_id
inner join
dbo.mobileCount as moc on ut.user_id=moc.user_id
left outer join
dbo.originalTweetCount as oc on ut.user_id=oc.user_id
left outer join
dbo.user_tweetscount as utc on ut.user_id=utc.user_id

where oc.oriTweetCnt>@twCountCritierior and oc.oriTweetCnt>@oritwCountCritierior

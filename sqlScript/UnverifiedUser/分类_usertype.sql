use SinaUnVerified
declare @twCountCritierior int
declare @oritwCountCritierior int


set @twCountCritierior=5
set @oritwCountCritierior=5

select avgCL.user_id,ut.name,avgCL.avgContentLength, ucl.min_len,
mec.mediaCount,CAST(mec.mediaCount as float)/oc.oriTweetCnt as mePercentage,
moc.mobileCount,CAST(moc.mobileCount as float)/utc.twCount as mbPercentage,
oc.oriTweetCnt,CAST(oc.oriTweetCnt as float)/utc.twCount as oriPercentage,
utc.twCount,ptd.timeDev,us.similarity,
utt.user_type
from 
dbo.users_unverified as ut 
left outer join
dbo.avgOriginalContentLength as avgCL on ut.user_id=avgCL.user_id
left outer join 
dbo.users_content_length as ucl on ut.user_id=ucl.user_id
left outer join
dbo.mediaCount as mec on ut.user_id=mec.user_id
inner join
dbo.mobileCount as moc on ut.user_id=moc.user_id
left outer join
dbo.originalTweetCount as oc on ut.user_id=oc.user_id
left outer join
dbo.user_tweetscount as utc on ut.user_id=utc.user_id
left outer join
dbo.postTimeDev as ptd on ut.user_id=ptd.user_id
left outer join
dbo.users_followers as uf on ut.user_id=uf.user_id
inner join
dbo.users_similarity as us on ut.user_id=us.user_id
inner join 
users_type as utt on ut.user_id=utt.user_id
where oc.oriTweetCnt>@twCountCritierior and oc.oriTweetCnt>@oritwCountCritierior 
and utt.user_type!=-1
order by uf.followers_count desc

use SinaVerified
declare @twCountCritierior int
set @twCountCritierior=5

select avgContentLength.user_id,avgContentLength.avgContentLength,mediaInformation.mediaPercentage,oriProduce.oriPercentage,thumbnailInfo.agg_facecount,mobileInfo.mobilePercentage,sutv.twCount,LEN(sutv.description) as desLength,thumbnailInfo.verified_type
from 
(
--找出用户发微博的平均字数
select su.user_id, AVG(CAST(LEN(s.content) as float)) as avgContentLength
from dbo.sample_users as su,
dbo.status as s
where su.user_id=s.user_id and s.retweeted_status_id is null
group by su.user_id) as avgContentLength,
(--超媒体携带率
select twCount.user_id,CAST(mediaCount.mediaCount as float)/CAST(twCount.tweetsCount as float) as mediaPercentage
from(
select su.user_id, COUNT(*) as tweetsCount
from dbo.sample_users as su,
dbo.status as s
where su.user_id=s.user_id and s.retweeted_status_id is null
group by su.user_id
) as twCount,
(
select su.user_id, 
CASE  when mediaProduce.mediaCount is NULL then 0
else mediaProduce.mediaCount
end as mediaCount
from SinaVerified.dbo.sample_users as su
left outer join
(
select su.user_id, COUNT(*) as mediaCount
from dbo.sample_users as su,
dbo.status as s
where su.user_id=s.user_id and (s.retweeted_status_id is null) and (ChARindex('http://t.cn/',s.content)>0 or s.original_pic!='')
group by su.user_id
)mediaProduce
on mediaProduce.user_id=su.user_id
) as mediaCount
where twCount.user_id=mediaCount.user_id
) as mediaInformation,

--原创率
(
select twCount.user_id,CAST(oriProduce.oriProduceCount as float)/CAST(twCount.tweetsCount as float) as oriPercentage
from(
select su.user_id, COUNT(*) as tweetsCount
from dbo.sample_users as su,
dbo.status as s
where su.user_id=s.user_id
group by su.user_id
) as twCount,
(
select su.user_id, 
CASE  when oriCount.oriProduceCount is NULL then 0
else oriCount.oriProduceCount
end as oriProduceCount
from SinaVerified.dbo.sample_users as su
left outer join
(
select su.user_id, COUNT(*) as oriProduceCount
from SinaVerified.dbo.sample_users as su,
SinaVerified.dbo.status as s
where su.user_id=s.user_id and (s.retweeted_status_id is null)
group by su.user_id
) oriCount
ON oriCount.user_id=su.user_id
) as oriProduce
where oriProduce.user_id=twCount.user_id
) as oriProduce,

(--头像是否分辨
select su.user_id, su.agg_facecount,
case 
	when u.verified_type=0 then 1
	else 2
end as verified_type
from dbo.sample_users as su,
dbo.users as u
where u.user_id=su.user_id
) as thumbnailInfo,

(
--手机发送率

select twCount.user_id,CAST(mobileCount.mobileCount as float)/CAST(twCount.tweetsCount as float) as mobilePercentage
from(
select su.user_id, COUNT(*) as tweetsCount
from dbo.sample_users as su,
dbo.status as s
where su.user_id=s.user_id
group by su.user_id
) as twCount,
(
select su.user_id, 
CASE  when mobileProduce.mobileCount is NULL then 0
else mobileProduce.mobileCount
end as mobileCount
from SinaVerified.dbo.sample_users as su
left outer join
(select su.user_id, COUNT(*) as mobileCount
from dbo.sample_users as su,
dbo.status as s,
dbo.sourceURL as surl
where su.user_id=s.user_id and s.status_id=surl.status_id and CHARINDEX('mobile',surl.source_url)>0
group by su.user_id)mobileProduce
on mobileProduce.user_id=su.user_id
) as mobileCount
where twCount.user_id=mobileCount.user_id
) as mobileInfo,
SinaVerified.dbo.sample_user_tweetscount_view as sutv
where avgContentLength.user_id=mediaInformation.user_id and avgContentLength.user_id=oriProduce.user_id and avgContentLength.user_id=thumbnailInfo.user_id and avgContentLength.user_id=mobileInfo.user_id and avgContentLength.user_id=sutv.user_id  and sutv.twCount>=@twCountCritierior


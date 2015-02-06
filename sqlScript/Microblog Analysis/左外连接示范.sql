--超媒体外连接

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

--原创外连接
select su.user_id, 
CASE  when oriCount.oriProduceCount is NULL then 0
else oriCount.oriProduceCount
end as oriProduceCount
from SinaVerified.dbo.sample_users as su
left outer join
(
select su.user_id, COUNT(*) as oriProduceCount
from SinaVerified.dbo.sample_users as su,
dbo.status as s
where su.user_id=s.user_id and (s.retweeted_status_id is null)
group by su.user_id
) oriCount
ON oriCount.user_id=su.user_id

--手机客户端外连接
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




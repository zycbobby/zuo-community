--先算转发量
use SinaUnverified


 if  OBJECT_ID( 'tempdb..##nobin') is not null
drop table tempdb..##nobin
go

select rc.retweet_count,
case when s.original_pic='' then 0
else 1 end as withPic
into ##nobin
from SinaUnverified.dbo.status_rt_cmt_verified as rc
inner join 
SinaUnverified.dbo.status_mix_verified as s

on rc.status_id=s.status_id
where rc.status_id<3350733374983436
order by NEWID()


select COUNT(*) from ##nobin
where withPic=1



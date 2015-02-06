--先算转发量
use SinaUnverified


 if  OBJECT_ID( 'tempdb..##nobin') is not null
drop table tempdb..##nobin
go

select top 5000 rc.retweet_count,
case when s.original_pic='' then 0
else 1 end as withPic

from SinaUnverified.dbo.status_rt_cmt as rc
inner join 
SinaUnverified.dbo.status as s
on rc.status_id=s.status_id
where s.original_pic!=''
order by NEWID()

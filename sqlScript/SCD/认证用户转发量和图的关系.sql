--先算转发量
use SinaUnverified


 if  OBJECT_ID( 'tempdb..##bin') is not null
drop table tempdb..##bin
go

select rc.status_id,
case when rc.retweet_count<=10 then 1
when rc.retweet_count>10 and rc.retweet_count<=50 then 2
when rc.retweet_count>50 and rc.retweet_count<=100 then 3
when rc.retweet_count>100 and rc.retweet_count<=1000 then 4
when rc.retweet_count>1000 then 5
end as binCount,
case when s.original_pic='' then 0
else 1 end as withPic
into ##bin

from SinaUnverified.dbo.status_rt_cmt_verified as rc
inner join 
SinaUnverified.dbo.status_mix_verified as s
on rc.status_id=s.status_id



select binCount,COUNT(*) as status_count,
SUM(withPic) as pic_count
 from ##bin 
 group by binCount order by binCount 
 
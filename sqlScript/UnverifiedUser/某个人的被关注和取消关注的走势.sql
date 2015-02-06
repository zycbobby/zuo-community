
declare @uid bigint
--方舟子
--set @uid=1195403385

--林书豪--really interesting
--set @uid=2106855375

--刘谦
--set @uid=1271542887

--新浪NBA驻华盛顿特派记者沈洋
--set @uid=1822851445

--韩寒
--set @uid=1191258123

--李娜
--set @uid=1746274673

--刘冬
--set @uid=1759228037

--如果两个人的曲线有相像之处，会不会是有关的呢？

--侯逸凡
set @uid=2424084591

select convert(varchar(10),ur.update_time,111),SUM(ur.follow),SUM(ur.unfollow)
from SinaUnVerified.dbo.user_relation as ur
where ur.target_user_id=@uid and ur.update_time>'2012-1-18'
group by convert(varchar(10),ur.update_time,111)
order by convert(varchar(10),ur.update_time,111) asc

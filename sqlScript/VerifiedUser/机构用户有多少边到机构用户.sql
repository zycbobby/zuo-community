--机构到机构
select ur.source_user_id,u1.screen_name, COUNT(*) as rToOg, rCount.rCnt
from SinaVerified.dbo.user_relation as ur,
SinaVerified.dbo.users as u1,
SinaVerified.dbo.users as u2,
(select ur.source_user_id,COUNT(*) as rCnt
from SinaVerified.dbo.user_relation as ur
group by ur.source_user_id
having COUNT(*)>10
) as rCount
where ur.source_user_id=u1.user_id  and u1.verified_type>0 and u1.verified_type<8 and 
ur.target_user_id=u2.user_id and u2.verified_type>0 and u2.verified_type<8
and ur.source_user_id=rCount.source_user_id
group by ur.source_user_id, u1.screen_name,rCount.rCnt
order by COUNT(*)/rCnt desc

--机构到个人
select ur.source_user_id,u1.screen_name, COUNT(*) as rToOg, rCount.rCnt
from SinaVerified.dbo.user_relation as ur,
SinaVerified.dbo.users as u1,
SinaVerified.dbo.users as u2,
(select ur.source_user_id,COUNT(*) as rCnt
from SinaVerified.dbo.user_relation as ur
group by ur.source_user_id
having COUNT(*)>10
) as rCount
where ur.source_user_id=u1.user_id  and u1.verified_type>0 and u1.verified_type<8 and 
ur.target_user_id=u2.user_id and u2.verified_type=0
and ur.source_user_id=rCount.source_user_id
group by ur.source_user_id, u1.screen_name,rCount.rCnt
order by COUNT(*)/rCnt desc
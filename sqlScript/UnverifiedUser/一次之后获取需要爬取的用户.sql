select *
from SinaUnverified.dbo.users as u 
(
select source_user_id, MAX(update_time) as max_time
from SinaUnverified.dbo.user_relation as ur
group  by source_user_id
) as urt 
where  u.user_id=urt.source_user_id  and urt.max_time<'2012-1-15' and u.followers_count>100 and u.friends_count<1000
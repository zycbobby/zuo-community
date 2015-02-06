/*
所谓我需要的用户就是

他有足够的关系数，以至于在网络里头他不是任何形式的孤立节点

并且有超过一定数量的原创微博，对我后面的分析不会造成太多空值方面的影响

*/

/*先从关系数做起*/

with verifiedRelation as (
select urc.source_user_id, urc.target_user_id
from SinaVerified.dbo.user_relation_c as urc 
inner join SinaVerified.dbo.users as u1 on urc.source_user_id=u1.user_id and u1.verified_type>0 and u1.verified_type<8
inner join SinaVerified.dbo.users as u2 on urc.target_user_id=u2.user_id and u2.verified_type>0 and u2.verified_type<8
),
followCount as (select urc.source_user_id as user_id, COUNT(*) as follow_count
from verifiedRelation as urc 
/*inner join SinaVerified.dbo.users as u on urc.source_user_id=u.user_id and u.verified_type>0 and u.verified_type<8*/
group  by urc.source_user_id
),
followerCount as (
select urc.target_user_id as user_id, COUNT(*) as follower_count
from verifiedRelation as urc
group  by urc.target_user_id
),
relationCount as (
select ferc.user_id, ferc.follower_count,fc.follow_count,COUNT(*) as ori_status_count
from followerCount as ferc full outer join followCount as fc on ferc.user_id=fc.user_id
inner join SinaVerified.dbo.status as s on ferc.user_id=s.user_id and s.retweeted_status_id is null
group by ferc.user_id, ferc.follower_count, fc.follow_count)

,relationSumCount as (
select rc.user_id, 
case rc.follower_count when null then 0 else rc.follower_count end as fecount,
case rc.follow_count when null then 0 else rc.follow_count end as fcount,
rc.ori_status_count
from relationCount as rc)

select rsc.user_id, u.name,rsc.fecount+rsc.fecount as relation_count, rsc.ori_status_count
from relationSumCount as rsc inner join SinaVerified.dbo.users as u on rsc.user_id=u.user_id
order by relation_count desc

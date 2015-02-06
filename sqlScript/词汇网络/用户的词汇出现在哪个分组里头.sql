
--目的是什么：
--用户词汇和分组的连接情况，用户掉在确定的组别的次数

WITH groupSummary AS
(select u.user_id, u.name as user_name,gi.group_id, COUNT(*) as group_count
from SinaVerified.dbo.status_noun as sn
inner join SinaVerified.dbo.status as s on sn.status_id=s.status_id
inner join SinaVerified.dbo.users as u on u.user_id=s.user_id
inner join stat.dbo.groupinfo2 as gi on gi.noun_id=sn.noun_id
group by u.user_id,u.name,gi.group_id
)
select * from groupSummary
/*
select gs.user_id, gs.name,gs.group_id, gs.groupCount
from (
select user_id,MAX(groupCount)  as maxGroupCount
from groupSummary
group by user_id
) as t
inner join groupSummary as gs on t.user_id=gs.user_id and t.maxGroupCount=gs.groupCount
where gs.groupCount>10
order by gs.group_id
*/

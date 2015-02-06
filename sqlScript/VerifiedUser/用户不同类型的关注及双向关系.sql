use SinaVerified

if OBJECT_ID('tempdb..##bi_r') is not null
	drop table tempdb..##bi_r



go 

select ur.source_user_id,ut2.type, 
case when COUNT(*) is null then 0
else COUNT(*) end as verifiedFriendsCount, SUM(ut.type) as oFriendsCount
from dbo.user_relation as ur left outer join SinaVerified.dbo.users_type as ut on ur.target_user_id=ut.user_id
inner join dbo.users_type as ut2 on ur.source_user_id=ut2.user_id
group by ur.source_user_id,ut2.type


select t.id1,t.id2
into ##bi_r
from
(select br.source_user_id as id1,br.target_user_id as id2
from dbo.bi_relation as br
union
select br.target_user_id as id1,br.source_user_id as id2
from dbo.bi_relation as br) as t


select br.id1,ut2.type, COUNT(*) as biCount, SUM(ut1.type) as obiCount
from ##bi_r as br inner join dbo.users_type as ut1 on br.id2=ut1.user_id
inner join dbo.users_type as ut2 on br.id1=ut2.user_id
group by br.id1,ut2.type
declare @uid bigint

set @uid=1083599615

select *
from SinaVerified.dbo.users
where user_id=@uid

select *
from SinaVerified.dbo.status
where user_id=@uid and retweeted_status_id is null


--他有的双向关系
select br.*, sut.type,tut.type,u1.name,u2.name
from SinaVerified.dbo.bi_relation as br
inner join
SinaVerified.dbo.users_type as sut
on br.source_user_id=sut.user_id
inner join 
SinaVerified.dbo.users_type as tut
on br.target_user_id=tut.user_id
inner join
SinaVerified.dbo.users as u1
on br.source_user_id=u1.user_id
inner join
SinaVerified.dbo.users as u2
on br.target_user_id=u2.user_id
where br.source_user_id=@uid or br.target_user_id=@uid

select COUNT(*) as verifiedFriendsCount
from SinaVerified.dbo.user_relation as ur where ur.source_user_id=@uid
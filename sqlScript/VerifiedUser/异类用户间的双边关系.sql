select br.source_user_id, sut.type,u1.name,br.target_user_id, tut.type,u2.name
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
where sut.type!=tut.type
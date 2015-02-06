declare @id1 bigint
declare @id2 bigint

set @id1=12
set @id2=932

select sn1.noun_id, sn2.noun_id,n1.word, n2.word,s.user_id
from SinaVerified.dbo.status_noun as sn1
inner join SinaVerified.dbo.status_noun as sn2 on sn1.status_id=sn2.status_id
inner join SinaVerified.dbo.status as s on s.status_id=sn1.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id
inner join SinaVerified.dbo.nouns as n1 on sn1.noun_id=n1.noun_id
inner join SinaVerified.dbo.nouns as n2 on sn2.noun_id=n2.noun_id
where sn1.noun_id=@id1 and sn2.noun_id=@id2
order by s.user_id 

declare @idf int
set @idf=3

declare @count int
set @count=2

set NOCOUNT ON

--保证这组词汇来源于不同的用户
select sn1.noun_id, sn2.noun_id, COUNT(distinct u.user_id)
from SinaVerified.dbo.status_noun as sn1
inner join SinaVerified.dbo.status_noun as sn2 on sn1.status_id=sn2.status_id
inner join SinaVerified.dbo.status as s on s.status_id=sn1.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id
where sn1.noun_id<sn2.noun_id and sn1.idf>@idf and sn2.idf>@idf
group by sn1.noun_id, sn2.noun_id
having count(distinct u.user_id)>@count
order by count(distinct u.user_id) desc



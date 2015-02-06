declare @uid1 bigint
declare @uid2 bigint

set @uid1=1885387520
set @uid2=1940053632

select s.content, n.word, sn.attr,sn.idf from 
SinaVerified.dbo.status as s inner join SinaVerified.dbo.status_noun as sn on s.status_id=sn.status_id
inner join SinaVerified.dbo.nouns as n on n.noun_id=sn.noun_id
where s.user_id=@uid1 and sn.idf>3
order by s.status_id


select s.content, n.word, sn.attr,sn.idf from 
SinaVerified.dbo.status as s inner join SinaVerified.dbo.status_noun as sn on s.status_id=sn.status_id
inner join SinaVerified.dbo.nouns as n on n.noun_id=sn.noun_id
where s.user_id=@uid2 --and sn.idf>3
order by s.status_id
go
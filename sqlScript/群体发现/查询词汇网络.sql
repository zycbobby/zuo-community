--查询词汇网络的情况

select gi.*, n.word
from stat.dbo.groupinfo2 as gi  inner join SinaVerified.dbo.nouns as n on gi.noun_id=n.noun_id

order by group_id
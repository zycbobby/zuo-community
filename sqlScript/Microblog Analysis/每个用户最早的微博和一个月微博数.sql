--这些id值得再挖一挖

select crawlRecord.tweetsCount,crawlRecord.EarliestCreated,u.screen_name,u.*
from
(
select count(*) as tweetsCount ,MIN(s.created_at) as EarliestCreated,s.user_id                                                                                                                            
from SinaVerified.dbo.status as s

group by s.user_id
--order by mcreated desc

) as crawlRecord,SinaVerified.dbo.users as u
where crawlRecord.tweetsCount>200 and crawlRecord.EarliestCreated>'2011-8-23' and crawlRecord.user_id=u.user_id
order by crawlRecord.EarliestCreated desc
go



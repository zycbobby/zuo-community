



 if  OBJECT_ID( 'tempdb..##source_url_with_mbit ') is not null
drop table tempdb..##source_url_with_mbit


select surl.status_id,
case when CHARINDEX('mobile',surl.source_url)>0 then 1
else 0
end as isM
into source_url_with_mbit
from SinaVerified.dbo.sourceURL as surl


create index sidAndBitIndex on source_url_with_mbit(status_id,isM)

--create index sidIndex on ##source_url_with_mbit(isM)
go
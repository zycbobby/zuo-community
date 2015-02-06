use SinaVerified
--平均每条微博会@多少人
if OBJECT_ID('tempdb..##Ated') is not null
begin
	print 'in'
	drop table ##Ated;
end
GO
--AT过多少人
if OBJECT_ID('tempdb..##AtedDisPeople') is not null
begin
	print 'in'
	drop table ##AtedDisPeople;
end
GO

--还要算出他们的At人的次数
select sidCnt.source_user_id as user_id,
case when sidCnt.cnt is null then 0
else sidCnt.cnt end as cnt
into ##Ated 
from (select at.source_user_id, COUNT(at.status_id)  as cnt
from SinaVerified.dbo.at_relation as at
group by at.source_user_id
) as sidCnt

--At过多少人
select atDisidCount.user_id, case when atDisidCount.cnt is null then 0 else atDisidCount.cnt end as cnt
into ##AtedDisPeople
 from 
(
select ar.source_user_id as user_id,COUNT(distinct ar.target_user_id) as cnt
from SinaVerified.dbo.at_relation as ar
group by ar.source_user_id) as atDisidCount


select mo5.user_id,u.screen_name,mo5.user_type,ated.cnt,mo5.tweetCount,ated.cnt*1.0/mo5.tweetCount, atdisp.cnt
from dbo.MiningOri5 as mo5
inner join ##Ated as ated on mo5.user_id=ated.user_id
inner join ##AtedDisPeople as atdisp on mo5.user_id=atdisp.user_id
inner join dbo.users as u on mo5.user_id=u.user_id
where mo5.user_type=1
GO
if OBJECT_ID('tempdb..##sids') is not null
begin
	print 'in'
	drop table ##sids;
end

if OBJECT_ID('tempdb..##tids') is not null
begin
	print 'in'
	drop table ##tids;
end
GO

--被At了多少次
if OBJECT_ID('tempdb..##BeAted') is not null
begin
	print 'in'
	drop table ##BeAted;
end
GO
--At过多少次
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
--被多少人AT过
if OBJECT_ID('tempdb..##BeDispeopleAted') is not null
begin
	print 'in'
	drop table ##BeDispeopleAted;
end
GO

--create table ##sids (status_id bigint);
--create table ##tids (target_user_id bigint);
GO
declare @uid bigint
set @uid=2043849437





select status_id
into ##sids
from SinaVerified.dbo.at_relation
where target_user_id=@uid


           select distinct target_user_id, count(*)
           from SinaVerified.dbo.at_relation as ar 
           where ar.status_id in (select * from ##sids) and ar.target_user_id!=@uid
           group by ar.target_user_id
           having count(*)>1
           

select distinct target_user_id
into ##tids
from SinaVerified.dbo.at_relation as ar
where ar.status_id in (select * from ##sids)

select ar1.target_user_id,ar2.target_user_id, ut1.type,ut2.type,u1.screen_name,u2.screen_name, COUNT(*)
from SinaVerified.dbo.at_relation as ar1 inner join SinaVerified.dbo.users_type as ut1 on ar1.target_user_id=ut1.user_id inner join SinaVerified.dbo.users as u1 on ar1.target_user_id=u1.user_id,
SinaVerified.dbo.at_relation as ar2 inner join SinaVerified.dbo.users_type as ut2 on ar2.target_user_id=ut2.user_id inner join SinaVerified.dbo.users as u2 on ar2.target_user_id=u2.user_id
where ar1.target_user_id in (select * from ##tids) and 
ar2.target_user_id in (select * from ##tids) and 
ar1.target_user_id<ar2.target_user_id and
ar1.target_user_id!=ar2.target_user_id and
ar1.status_id=ar2.status_id
group by ar1.target_user_id,ar2.target_user_id,ut1.type,ut2.type,u1.screen_name,u2.screen_name

--还要算出他们的At人的次数
select t.target_user_id as user_id, 
case when sidCnt.cnt is null then 0
else sidCnt.cnt end as cnt
into ##Ated 
from (select at.source_user_id, COUNT(at.status_id)  as cnt
from SinaVerified.dbo.at_relation as at
right outer join ##tids as t on at.source_user_id=t.target_user_id
group by at.source_user_id
) as sidCnt
right outer join ##tids as t on sidCnt.source_user_id=t.target_user_id




--还要算出他们的被At次数
select t.target_user_id as user_id, 
case when sidCnt.cnt is null then 0
else sidCnt.cnt end as cnt
into ##BeAted 
from (select at.target_user_id as user_id, COUNT(at.status_id)  as cnt
from SinaVerified.dbo.at_relation as at
right outer join ##tids as t on at.target_user_id=t.target_user_id
group by at.target_user_id
) as sidCnt
right outer join ##tids as t on sidCnt.user_id=t.target_user_id



--At过多少人
select t.target_user_id as user_id, case when atDisidCount.cnt is null then 0 else atDisidCount.cnt end as cnt
into ##AtedDisPeople
 from 
(
select ar.source_user_id as user_id,COUNT(distinct ar.target_user_id) as cnt
from SinaVerified.dbo.at_relation as ar
where ar.source_user_id in (select * from ##tids)
group by ar.source_user_id) as atDisidCount
right outer join ##tids as t on atDisidCount.user_id=t.target_user_id


--被多少人AT
select t.target_user_id as user_id, case when beatDisidCount.cnt is null then 0 else beatDisidCount.cnt end as cnt
into ##BeDispeopleAted
 from 
(
select ar.target_user_id as user_id,COUNT(distinct ar.source_user_id) as cnt
from SinaVerified.dbo.at_relation as ar
where ar.target_user_id in (select * from ##tids)
group by ar.target_user_id) as beatDisidCount
right outer join ##tids as t on beatDisidCount.user_id=t.target_user_id




select ut.user_id,u.screen_name,ut.type, ated.cnt as atCnt, beated.cnt as beatCnt,
adp.cnt as AtPeopleCnt, badp.cnt as bePeopleAtCnt
from ##tids as t
inner join SinaVerified.dbo.users_type as ut on t.target_user_id=ut.user_id
inner join ##Ated as ated on t.target_user_id=ated.user_id
inner join ##BeAted as beated on t.target_user_id=beated.user_id
inner join SinaVerified.dbo.users as u on ut.user_id=u.user_id
inner join ##AtedDisPeople  as adp on ut.user_id=adp.user_id
inner join ##BeDispeopleAted  as badp on ut.user_id=badp.user_id
order by ut.type

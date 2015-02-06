/****** Script for SelectTopNRows command from SSMS  ******/

--一共是39891个用户

SELECT u.verified_type, COUNT(distinct u.user_id)
from SinaVerified.dbo.words_all_ou_verified as w
inner join SinaVerified.dbo.status as s on w.status_id=s.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id
group by u.verified_type

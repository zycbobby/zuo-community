/****** Script for SelectTopNRows command from SSMS  ******/
SELECT top 1000 u.usertype
from SinaVerified.dbo.words_all_ou_verified as w
inner join SinaVerified.dbo.status as s on w.status_id=s.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id

select s.user_id, ut.type,(DATEPART(M, s.created_at)-8)*31+DATEPART(D, s.created_at)-20 as daysPast,COUNT(*)
from SinaVerified.dbo.status as s inner join SinaVerified.dbo.users_type as ut on s.user_id=ut.user_id
group by s.user_id,ut.type,((DATEPART(M, s.created_at)-8)*31+DATEPART(D, s.created_at)-20)
order by s.user_id,((DATEPART(M, s.created_at)-8)*31+DATEPART(D, s.created_at)-20)
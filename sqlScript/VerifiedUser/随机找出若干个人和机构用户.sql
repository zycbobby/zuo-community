
declare @t table
(
rowId int,
uid bigint,
user_type int
);

with pAndo 
as
(
select top 1000 ut.*
from SinaVerified.dbo.users_type as ut
where ut.type=0
order by NEWID()
union 
select top 1000 ut.*
from SinaVerified.dbo.users_type as ut
where ut.type=1
order  by NEWID()
)




insert into @t select ROW_NUMBER() over(order by pAndo.type),pAndo.*  from pAndo

select * from @t

select t1.rowId,t2.rowId from SinaVerified.dbo.user_relation as ur inner join @t as t1 on ur.source_user_id=t1.uid
inner join @t as t2 on ur.target_user_id=t2.uid




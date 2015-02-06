declare @f bit
set @f=0


if @f=1
begin
delete from SinaVerified.dbo.status
where status_id>3415643573514472
end

go

select COUNT(s.status_id)
from SinaVerified.dbo.status as s
--where s.status_id=3424310041970567
where s.status_id>3415643573514472


select s.*
from SinaVerified.dbo.status as s
--where s.status_id=3424310041970567
where s.user_id=1663429634	 and s.status_id>3415643573514472
order by s.status_id asc


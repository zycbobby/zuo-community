/*
select MAX(rt.status_id)
from SinaUnverified.dbo.status_rt_cmt as rt

3350733374983436
*/
/*
select MAX(status_id)
from SinaUnverified.dbo.status_rt_cmt_verified as rt
3358630846782417
*/


select COUNT(*)
from SinaUnverified.dbo.status_rt_cmt as rt

select COUNT(*)
from SinaUnverified.dbo.status_rt_cmt_verified as rt
SELECT status_id
  FROM [SinaUnverified].[dbo].[status_mix_verified]
  order by status_id
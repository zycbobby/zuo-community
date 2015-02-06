--必须要在 222.200.181.241 上面的数据库执行
select urc.*,u1.name, u2.name
from SinaVerified.dbo.user_relation_c as urc
inner join SinaVerified.dbo.users as u1 on urc.source_user_id= u1.user_id and u1.verified_type>0 and u1.verified_type<8
inner join SinaVerified.dbo.users as u2 on urc.target_user_id= u2.user_id and u2.verified_type>0 and u2.verified_type<8

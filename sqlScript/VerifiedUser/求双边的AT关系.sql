select ur1.source_user_id,ur1.target_user_id,ut1.type,ut2.type
from SinaVerified.dbo.at_relation as ur1
inner join 
SinaVerified.dbo.at_relation as ur2
on ur1.source_user_id=ur2.target_user_id 
and ur1.target_user_id=ur2.source_user_id
 and ur1.source_user_id<ur2.source_user_id
 inner join
 SinaVerified.dbo.users_type as ut1
 on 
 ut1.user_id=ur1.source_user_id
 inner join
 SinaVerified.dbo.users_type as ut2
 on 
 ut2.user_id=ur2.source_user_id
 inner join
 SinaVerified.dbo.source_url_with_clientbit as urlc1
 on urlc1.status_id=ur1.status_id
 inner join
 SinaVerified.dbo.source_url_with_clientbit as urlc2
 on urlc2.status_id=ur2.status_id
 where 
 ut1.type!=ut2.type and 
 urlc1.clientbit=1 and urlc2.clientbit=1
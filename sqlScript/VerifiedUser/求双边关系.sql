


select ur1.source_user_id,ur1.target_user_id
from SinaVerified.dbo.user_c_relation as ur1
inner join 
SinaVerified.dbo.user_c_relation as ur2
on ur1.source_user_id=ur2.target_user_id and ur1.target_user_id=ur2.source_user_id and ur1.source_user_id<ur2.source_user_id
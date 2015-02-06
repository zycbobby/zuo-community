select ufors.type,COUNT(*) as cnt
from SinaVerified.dbo.user_relation as ur
inner join 
SinaVerified.dbo.users_type as  u on ur.target_user_id=u.user_id
inner join
SinaVerified.dbo.originalTweetCount as otc on ur.target_user_id=otc.user_id
inner join 
SinaVerified.dbo.users_type as  ufors
on ur.source_user_id=ufors.user_id
where ur.target_user_id in (1769565753,1658351742,1718149035,2230604923,2275959650,1359729437,1917597681,1877705801,1701255031)
and otc.oriTweetCnt>=5
group by ufors.type

go

select ur.source_user_id, ufors.type
                        from SinaVerified.dbo.user_relation as ur       
                        inner join        
                        SinaVerified.dbo.users_type as  u 
                        on ur.target_user_id=u.user_id        
                        inner join
                        SinaVerified.dbo.originalTweetCount as otc 
                        on ur.target_user_id=otc.user_id
                        inner join 
                        SinaVerified.dbo.users_type as  ufors
                        on ur.source_user_id=ufors.user_id
                        where ur.target_user_id in (1769565753,1658351742,1718149035,2230604923,2275959650,1359729437,1917597681,1877705801,1701255031) and otc.oriTweetCnt>=5

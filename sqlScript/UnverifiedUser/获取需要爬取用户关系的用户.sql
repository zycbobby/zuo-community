select *
from SinaUnverified.dbo.users as u
where u.followers_count>100 and u.friends_count<1000 and u.friends_count>100
select u.user_id,u.name,u.screen_name,u.description,u.usertype
into SinaVerified.dbo.sample_users
from SinaVerified.dbo.users as u
where u.usertype=1 or u.usertype=2
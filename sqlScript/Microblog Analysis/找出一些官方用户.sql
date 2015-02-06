SELECT  distinct   u.user_id, screen_name, name, description, usertype
FROM         SinaVerified.dbo.users AS u,
SinaVerified.dbo.status as s

WHERE     ((CHARINDEX('¹Ù·½', description) > 0) or (CHARINDEX('ÍøÕ¾', description) > 0) or
(CHARINDEX('ÂÛÌ³', description) > 0) ) and u.user_id in (select user_id from SinaVerified.dbo.status) and usertype is null
GO

select COUNT(*)
from SinaVerified.dbo.users
where usertype=2
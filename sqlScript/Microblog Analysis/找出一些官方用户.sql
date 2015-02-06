SELECT  distinct   u.user_id, screen_name, name, description, usertype
FROM         SinaVerified.dbo.users AS u,
SinaVerified.dbo.status as s

WHERE     ((CHARINDEX('�ٷ�', description) > 0) or (CHARINDEX('��վ', description) > 0) or
(CHARINDEX('��̳', description) > 0) ) and u.user_id in (select user_id from SinaVerified.dbo.status) and usertype is null
GO

select COUNT(*)
from SinaVerified.dbo.users
where usertype=2
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT br.*
  FROM [SinaVerified].[dbo].[bi_relation] as br inner join SinaVerified.dbo.users as u1
  on br.source_user_id=u1.user_id and u1.verified_type>0 and u1.verified_type<8
  inner join SinaVerified.dbo.users as u2
  on br.target_user_id=u2.user_id and u2.verified_type>0 and u2.verified_type<8
  
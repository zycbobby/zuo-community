--真不容易
select *
from wikidb.dbo.page as p
	inner join wikidb.dbo.revision as r on r.rev_id=p.page_latest
	inner join wikidb.dbo.text as t on t.old_id=r.rev_text_id
where p.page_title='沙坡头区'

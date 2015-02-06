
select top 100 master.sys.fn_varbintohexstr(old_text)
from wikidb.dbo.text
go

select top 100 convert(varchar,old_text)
from wikidb.dbo.text

go

select top 100 master.sys.fn_varbintohexstr(old_text)
from wikidb.dbo.text
go
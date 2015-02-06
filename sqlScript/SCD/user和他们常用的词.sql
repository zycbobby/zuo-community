if OBJECT_ID('tempdb..##wc') is not null
drop table tempdb..##wc
go
--出现该词的评论和转发次数
select s.user_id,u.screen_name,w.word,COUNT(w.status_id) as statusCount,SUM(rc.cmtCount) as scmt,SUM(rc.rtCount) as srt
into ##wc
from SinaVerified.dbo.words_all_ou_verified as w
inner join SinaVerified.dbo.status as s on w.status_id=s.status_id
inner join SinaVerified.dbo.users as u on s.user_id=u.user_id
inner join SinaVerified.dbo.rt_cmt as rc on s.status_id=rc.status_id
where len(w.word)>1 and w.attr!='en' and CHARINDEX(w.word, s.content)>0
group by s.user_id,u.screen_name,w.word

having count(w.status_id)>10
order by s.user_id

CREATE INDEX uidIndex
    ON ##wc ( user_id asc) 

CREATE INDEX wordIndex
    ON ##wc ( word) 

--select * from ##wc


--出现该词的微博举例
select wc.*, sw.statusWeek,s.content
from 
(
select wc.user_id, wc.word, MIN(s.status_id) as sid
from ##wc as wc
inner join SinaVerified.dbo.status as s on wc.user_id=s.user_id and CHARINDEX(wc.word, s.content)>0
group by wc.user_id, wc.word
) as t inner join ##wc as wc on t.user_id=wc.user_id and  t.word=wc.word
inner join SinaVerified.dbo.status as s on t.sid=s.status_id 
inner join 
--这个人这个星期的微博数
(
select s.user_id,COUNT(*) as statusWeek
from SinaVerified.dbo.status as s
where s.created_at>'2011-8-20' and s.created_at<'2011-8-27'
group by s.user_id
) as sw on wc.user_id=sw.user_id
--and s.retweeted_status_id is not null
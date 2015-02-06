--取消关注一般是取消谁（这个人是什么时候关注上的）
select uri1.source_user_id,uri1.target_user_id,DATEDIFF(DAY,MAX(uri1.update_time),MAX(uri2.update_time))
from SinaUnVerified.dbo.user_relation_inc as uri1,
SinaUnVerified.dbo.user_relation_inc as uri2
where uri1.source_user_id=uri2.source_user_id and uri1.target_user_id=uri2.target_user_id
and uri1.follow=1 and uri2.unfollow=1 and uri2.update_time>uri1.update_time
group by uri1.source_user_id,uri1.target_user_id,uri2.source_user_id,uri2.target_user_id
having MAX(uri2.update_time)>MAX(uri1.update_time)
order by DATEDIFF(DAY,MAX(uri1.update_time),MAX(uri2.update_time)) desc
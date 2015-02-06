with follower as
(
select urc.target_user_id, COUNT(*) as followers_count
from SinaUnverified.dbo.user_relation_c as urc
group by urc.target_user_id
)


select u.user_id, u.name,f.followers_count
from follower as f
inner join SinaUnverified.dbo.users as u on f.target_user_id = u.user_id
where u.verified=0
order by followers_count desc
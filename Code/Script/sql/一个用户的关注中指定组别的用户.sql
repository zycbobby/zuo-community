SELECT u.user_id,
       u.user_name,
       ugc.group_id
  FROM user_group_clustered AS ugc
       INNER JOIN users AS u
               ON ugc.user_id = u.user_id
       inner join followees as f
               on u.user_id=f.user_id
 WHERE ugc.group_id = 2
 ORDER BY u.user_name;

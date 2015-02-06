SELECT u.user_id,
       u.user_name,
       ugc.group_id
  FROM user_group_clustered AS ugc
       INNER JOIN users AS u
               ON ugc.user_id = u.user_id
 WHERE ugc.group_id = 0
 ORDER BY u.user_name;


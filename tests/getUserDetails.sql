<dtml-comment>
Connection_id : sufdb
arguments: name
</dtml-comment>
SELECT users.name as name, 
       users.password as password, 
       roles.role as role,
       users.extra1 as extra1,
       users.extra2 as extra2
FROM users,roles 
WHERE users.name=<dtml-sqlvar name type="string"> and users.name=roles.name
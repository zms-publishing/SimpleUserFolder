<dtml-comment>
Connection_id : sufdb
arguments: name
</dtml-comment>
SELECT users.name as NAME, users.password as PASSWORD, roles.role as ROLE FROM users,roles WHERE users.name=<dtml-sqlvar name type="string"> and users.name=roles.name
<dtml-comment>
Connection_id : sufdb
arguments: name
</dtml-comment>
SELECT * FROM users WHERE users.name=<dtml-sqlvar name type="string">
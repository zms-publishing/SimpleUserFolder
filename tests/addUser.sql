<dtml-comment>
Connection_id : sufdb
arguments: name password roles
</dtml-comment>
insert into users(name,password) values (<dtml-sqlvar name type="string">,<dtml-sqlvar password type="string">)
<dtml-var sql_delimiter>
<dtml-in roles>
insert into roles(name,role) values (<dtml-sqlvar name type="string">,<dtml-sqlvar sequence-item type="string">)
<dtml-unless sequence-end>
<dtml-var sql_delimiter>
</dtml-unless>
<dtml-else>
insert into roles(name,role) values (<dtml-sqlvar name type="string">,'')
</dtml-in>
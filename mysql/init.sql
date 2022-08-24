create database if not exists myjobhist;
use myjobhist;
create table if not exists jobhist
(
  jobid int not null primary key auto_increment,
  hist_id blob(16) not null,
  raw_data longblob not null
) default charset=utf8;


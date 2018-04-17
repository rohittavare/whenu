drop table if exists menu;
create table entries (
  id integer primary key autoincrement,
  name text not null,
  date text not null,
  hall text not null
);

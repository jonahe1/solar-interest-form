drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  name text not null,
  age text not null,
  address text not null,
  city text not null,
  state text not null,
  zip text not null,
  'text' text not null
);

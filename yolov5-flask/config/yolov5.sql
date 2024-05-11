create database login;

create table user
(
    id int auto_increment  primary key,
    username varchar(32) not null,
    password varchar(50) not null
)
    engine = InnoDB;
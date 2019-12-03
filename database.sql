
create database drive;
use drive;

create table users(
    id int primary key auto_increment,
    primaryName varchar(255),
    lastName varchar(255),
    email varchar(255),
    passwd varchar(255)
)engine=innoDB;


create table files(
    id int primary key auto_increment,
    filename varchar(255),
    filetype varchar(255),
    size int,
    date_upload date, 
    user_id int,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
)engine=innoDB;


create table shared(
    id int primary key auto_increment,
    date_shared date, 
    user_shared int,
    user_receive int,
    file_id int,
    
        
    FOREIGN KEY (user_shared)
        REFERENCES users(id),
        
    FOREIGN KEY (user_receive)
        REFERENCES users(id),

    FOREIGN KEY (file_id)
        REFERENCES files(id)
)engine=innoDB;



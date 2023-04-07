CREATE DATABASE crawl_database;
USE crawl_database;

CREATE TABLE Tablet(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Chip NVARCHAR(200),
    RAM NVARCHAR(200),
    Disk NVARCHAR(200),
    Screen NVARCHAR(200),
    OS NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Tablet_url ON Tablet(url);
CREATE TABLE Phone(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Chip NVARCHAR(200),
    RAM NVARCHAR(200),
    Disk NVARCHAR(200),
    Screen NVARCHAR(200),
    OS NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Phone_url ON Phone(url);
CREATE TABLE Laptop(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    CPU NVARCHAR(200),
    RAM NVARCHAR(200),
    Disk NVARCHAR(200),
    Screen NVARCHAR(200),
    OS NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Laptop_url ON Laptop(url);
CREATE TABLE PC(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    CPU NVARCHAR(200),
    RAM NVARCHAR(200),
    Disk NVARCHAR(200),
    Screen NVARCHAR(200),
    OS NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_PC_url ON PC(url);
CREATE TABLE Screen(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Screen_size NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Screen_url ON Screen(url);
CREATE TABLE Mouse(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    DPI NVARCHAR(200),
    Connect_type NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Mouse_url ON Mouse(url);
CREATE TABLE Keyboard(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Compatible NVARCHAR(200),
    Connect_type NVARCHAR(200),
    Size NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Keyboard_url ON Keyboard(url);
CREATE TABLE Smart_watch(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Screen NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Smart_watch_url ON Smart_watch(url);
CREATE TABLE Other(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Other_url ON Other(url);
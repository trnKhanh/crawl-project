CREATE DATABASE crawl_database;
USE crawl_database;

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
CREATE TABLE Earphone(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Compatible NVARCHAR(200),
    Connect_type NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Earphone_url ON Earphone(url);
CREATE TABLE Router(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Bandwidth NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Router_url ON Router(url);
CREATE TABLE LoudSpeaker(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_LoudSpeaker_url ON LoudSpeaker(url);
CREATE TABLE Other(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    url NVARCHAR(200),
    image_path NVARCHAR(200),
    website NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_Other_url ON Other(url);

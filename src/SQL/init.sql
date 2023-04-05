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
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_tablet_url ON tablet(url);
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
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_phone_url ON phone(url);
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
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_laptop_url ON laptop(url);
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
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_PC_url ON PC(url);
CREATE TABLE Screen(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Screen_type NVARCHAR(200),
    Screen_size NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_screen_url ON screen(url);
CREATE TABLE Mouse(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    DPI NVARCHAR(200),
    Connect_type NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_mouse_url ON mouse(url);
CREATE TABLE Keyboard(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Compatible NVARCHAR(200),
    Connect_type NVARCHAR(200),
    Size NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_keyboard_url ON keyboard(url);
CREATE TABLE Smart_Watch(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(200),
    Price INT,
    Screen NVARCHAR(200),
    Brand NVARCHAR(200),
    url NVARCHAR(200),
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_smart_watch_url ON smart_watch(url);
CREATE TABLE Other(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    url NVARCHAR(200),
    image_path NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_other_url ON other(url);
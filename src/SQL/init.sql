USE crawl_database;

CREATE TABLE tablet(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    chip NVARCHAR(200),
    ram NVARCHAR(200),
    disk NVARCHAR(200),
    screen NVARCHAR(200),
    OS NVARCHAR(200),
    url NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_tablet_url ON tablet(url);
CREATE TABLE computer(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    cpu NVARCHAR(200),
    ram NVARCHAR(200),
    disk NVARCHAR(200),
    screen NVARCHAR(200),
    OS NVARCHAR(200),
    url NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_computer_url ON computer(url);
CREATE TABLE screen(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    screen_type NVARCHAR(200),
    screen_size NVARCHAR(200),
    url NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_screen_url ON screen(url);
CREATE TABLE mouse(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    dpi NVARCHAR(200),
    connect_type NVARCHAR(200),
    brand NVARCHAR(200),
    url NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_mouse_url ON mouse(url);
CREATE TABLE keyboard(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    compatible NVARCHAR(200),
    connect_type NVARCHAR(200),
    size NVARCHAR(200),
    brand NVARCHAR(200),
    url NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_keyboard_url ON keyboard(url);
CREATE TABLE printer(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    printer_type NVARCHAR(200),
    print_speed NVARCHAR(200),
    ink_type NVARCHAR(200),
    print_quality NVARCHAR(200),
    paper_type NVARCHAR(200),
    brand NVARCHAR(200),
    url NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_printer_url ON printer(url);
CREATE TABLE watch(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    screen NVARCHAR(200),
    brand NVARCHAR(200),
    url NVARCHAR(200)
);
CREATE UNIQUE INDEX unique_watch_url ON watch(url);
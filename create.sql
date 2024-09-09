CREATE SCHEMA `flask_hello` ;
CREATE USER 'flask_hello_adm'@'%' IDENTIFIED BY 'miapassword1' ;
GRANT all privileges ON flask_hello.* TO 'flask_hello_adm'@'%';
FLUSH PRIVILEGES;
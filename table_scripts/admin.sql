use furlencode;
drop table admin;
CREATE TABLE `furlencode`.`admin` (
  `user` VARCHAR(100) NOT NULL,
  `password` VARCHAR(45) NULL,
  PRIMARY KEY (`user`));
INSERT INTO admin VALUES ('ajaybhat@gmail.com','ca17b00486adaeda98201aafc50113cb');

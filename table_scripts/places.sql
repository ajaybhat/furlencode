use furlencode;
drop table places;
CREATE TABLE `furlencode`.`places` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `description` VARCHAR(400) NULL,
  `pic` TEXT NULL,
  `category` VARCHAR(45) NULL,
  `latitude` DOUBLE NOT NULL,
  `longitude` DOUBLE NOT NULL,
  `time_from` VARCHAR(45) NULL,
  `time_to` VARCHAR(45) NULL,
  `place_uuid` VARCHAR(200) NULL,
  `place_is_good` BOOLEAN NULL,
  PRIMARY KEY (`id`));


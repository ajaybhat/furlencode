use furlencode;
drop table visited_places;
CREATE TABLE `furlencode`.`visited_places` (
  `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `place_id` INT NULL,
  `last_seen` LONG NULL,
  CONSTRAINT `place_uuid`
    FOREIGN KEY (`place_id`)
    REFERENCES `furlencode`.`places` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

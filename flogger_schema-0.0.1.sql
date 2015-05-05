-- SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
-- SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
-- SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
-- USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `users` ;

-- CREATE TABLE IF NOT EXISTS `mydb`.`users` (
CREATE TABLE IF NOT EXISTS users (
  `id` INT NULL DEFAULT NULL,
  `first_name` TEXT NULL DEFAULT NULL,
  `surname` TEXT NULL DEFAULT NULL,
  `phone` TEXT NULL DEFAULT NULL,
  `email` TEXT NULL DEFAULT NULL,
  `password` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
  UNIQUE (`email` ASC));


-- -----------------------------------------------------
-- Table `mydb`.`aircraft`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `aircraft` ;

CREATE TABLE IF NOT EXISTS `aircraft` (
  `id` INT NULL DEFAULT NULL,
  `registration` TEXT NULL DEFAULT NULL,
  `type` TEXT NULL DEFAULT NULL,
  `model` TEXT NULL DEFAULT NULL,
  `owner` TEXT NULL DEFAULT NULL,
  `airfield` TEXT NULL DEFAULT NULL,
  `flarm_id` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `mydb`.`flight_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flight_log` ;

CREATE TABLE IF NOT EXISTS `flight_log` (
  `id` INT NULL DEFAULT NULL,
  `sdate` TEXT NULL DEFAULT NULL,
  `stime` TEXT NULL DEFAULT NULL,
  `edate` TEXT NULL DEFAULT NULL,
  `etime` TEXT NULL DEFAULT NULL,
  `duration` TEXT NULL DEFAULT NULL,
  `src_callsign` TEXT NULL DEFAULT NULL,
  `max_altitude` TEXT NULL DEFAULT NULL,
  `speed` TEXT NULL DEFAULT NULL,
  'registration' TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `mydb`.`flight_group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flight_group` ;

CREATE TABLE IF NOT EXISTS `flight_group` (
  `id` INT NULL DEFAULT NULL,
  `groupID` TEXT NULL DEFAULT NULL,
  `sdate` TEXT NULL DEFAULT NULL,
  `stime` TEXT NULL DEFAULT NULL,
  `edate` TEXT NULL DEFAULT NULL,
  `etime` TEXT NULL DEFAULT NULL,
  `duration` TEXT NULL DEFAULT NULL,
  `src_callsign` TEXT NULL DEFAULT NULL,
  `max_altitude` TEXT NULL DEFAULT NULL,
  'registration' TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `mydb`.`launch_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `launch_types` ;

CREATE TABLE IF NOT EXISTS `launch_types` (
  `id` INT NOT NULL,
  `aero_tow` VARCHAR(45) NULL,
  `winch` VARCHAR(45) NULL,
  `self_launch` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
--ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`flights`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flights` ;

CREATE TABLE IF NOT EXISTS `flights` (
  `id` INT NULL DEFAULT NULL,
  `sdate` TEXT NULL DEFAULT NULL,
  `stime` TEXT NULL DEFAULT NULL,
  `edate` TEXT NULL DEFAULT NULL,
  `etime` TEXT NULL DEFAULT NULL,
  `duration` TEXT NULL DEFAULT NULL,
  `src_callsign` TEXT NULL DEFAULT NULL,
  `max_altitude` TEXT NULL DEFAULT NULL,
  'registration' TEXT NULL DEFAULT NULL,
  `aircraft_id` INT NOT NULL,
  `users_id` INT NOT NULL,
  `launch_type` INT NOT NULL,
  `launch_types_idlaunch_types` INT NOT NULL,
  PRIMARY KEY (`id`),
--  INDEX `fk_flights_aircraft_idx` (`aircraft_id` ASC),
--  INDEX `fk_flights_users1_idx` (`users_id` ASC),
--  INDEX `fk_flights_launch_types1_idx` (`launch_types_idlaunch_types` ASC),
  CONSTRAINT `fk_flights_aircraft`
    FOREIGN KEY (`aircraft_id`)
    REFERENCES `aircraft` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_flights_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_flights_launch_types1`
    FOREIGN KEY (`launch_types_idlaunch_types`)
    REFERENCES `launch_types` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`flight_log_final`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `flight_log_final` ;

CREATE TABLE IF NOT EXISTS `flight_log_final` (
  `id` INT NULL DEFAULT NULL,
  `sdate` TEXT NULL DEFAULT NULL,
  `stime` TEXT NULL DEFAULT NULL,
  `edate` TEXT NULL DEFAULT NULL,
  `etime` TEXT NULL DEFAULT NULL,
  `duration` TEXT NULL DEFAULT NULL,
  `src_callsign` TEXT NULL DEFAULT NULL,
  `max_altitude` TEXT NULL DEFAULT NULL,
  `speed` TEXT NULL DEFAULT NULL,
  `registration` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`));


--SET SQL_MODE=@OLD_SQL_MODE;
--SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
--SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

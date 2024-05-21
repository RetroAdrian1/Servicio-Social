-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema serviciosocial
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema serviciosocial
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `serviciosocial` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `serviciosocial` ;

-- -----------------------------------------------------
-- Table `serviciosocial`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `correo` VARCHAR(45) NULL DEFAULT NULL,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  `contraseña` VARCHAR(255) NULL DEFAULT NULL,
  `rol` VARCHAR(45) NULL DEFAULT NULL,
  `clinica` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`superadmin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`superadmin` (
  `idsuperAdmin` VARCHAR(20) NOT NULL,
  `usuariosuperAdmin` VARCHAR(20) NOT NULL,
  `password_hashsuperAdmin` VARCHAR(250) NOT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idsuperAdmin`),
  INDEX `FK_superAdmin_Usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_superAdmin_Usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`adminfisioterapia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`adminfisioterapia` (
  `idAdminFisioterapia` VARCHAR(45) NOT NULL,
  `nombreAdminFisioterapia` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioAdminFisioterapia` VARCHAR(45) NOT NULL,
  `contraseñaAdminFisioterapia` VARCHAR(255) NOT NULL,
  `idSuperAdmin_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idAdminFisioterapia`),
  INDEX `FK_adminFisioterapia_superAdmin` (`idSuperAdmin_FK` ASC) INVISIBLE,
  INDEX `FK_adminFisioterapia_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_adminFisioterapia_superAdmin`
    FOREIGN KEY (`idSuperAdmin_FK`)
    REFERENCES `serviciosocial`.`superadmin` (`idsuperAdmin`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_adminFisioterapia_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`adminodontologia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`adminodontologia` (
  `idAdminOdontologia` VARCHAR(45) NOT NULL,
  `nombreAdminOdontologia` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioAdminOdontologia` VARCHAR(45) NOT NULL,
  `contraseñaAdminOdontologia` VARCHAR(255) NOT NULL,
  `idSuperAdmin_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idAdminOdontologia`),
  INDEX `FK_adminOdontologia_superAdmin_idx` (`idSuperAdmin_FK` ASC) VISIBLE,
  INDEX `FK_adminOdontologia_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_adminOdontologia_superAdmin`
    FOREIGN KEY (`idSuperAdmin_FK`)
    REFERENCES `serviciosocial`.`superadmin` (`idsuperAdmin`),
  CONSTRAINT `FK_adminOdontologia_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`adminoptometria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`adminoptometria` (
  `idAdminOptometria` VARCHAR(45) NOT NULL,
  `nombreAdminOptometria` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioAdminOptometria` VARCHAR(45) NOT NULL,
  `contraseñaAdminOptometria` VARCHAR(255) NOT NULL,
  `idSuperAdmin_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idAdminOptometria`),
  INDEX `FK_adminOptometria_superAdmin_idx` (`idSuperAdmin_FK` ASC) VISIBLE,
  INDEX `FK_adminOptometria_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_adminOptometria_superAdmin`
    FOREIGN KEY (`idSuperAdmin_FK`)
    REFERENCES `serviciosocial`.`superadmin` (`idsuperAdmin`),
  CONSTRAINT `FK_adminOptometria_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`profesorfisioterapia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`profesorfisioterapia` (
  `rfcProfesorFisioterapia` VARCHAR(45) NOT NULL,
  `nombreProfesorFisioterapia` VARCHAR(45) NULL DEFAULT NULL,
  `apellidosProfesorFisioterapia` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioProfesorFisioterapia` VARCHAR(45) NOT NULL,
  `contraseñaProfesorFisioterapia` VARCHAR(255) NOT NULL,
  `idAdminFisioterapia_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`rfcProfesorFisioterapia`),
  INDEX `FK_profesoFisioterapia_adminFisioterapia` (`idAdminFisioterapia_FK` ASC) INVISIBLE,
  INDEX `FK_profesorFisioterapia_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_profesorFisioterapia_adminFisioterapia`
    FOREIGN KEY (`idAdminFisioterapia_FK`)
    REFERENCES `serviciosocial`.`adminfisioterapia` (`idAdminFisioterapia`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_profesorFisioterapia_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`alumnofisioterapia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`alumnofisioterapia` (
  `numeroCuentaAlumnoFisioterapia` VARCHAR(45) NOT NULL,
  `nombreAlumnoFisioterapia` VARCHAR(45) NULL DEFAULT NULL,
  `apellidosAlumnoFisioterapia` VARCHAR(45) NULL DEFAULT NULL,
  `año` VARCHAR(10) NULL DEFAULT NULL,
  `asignaturaFisioterapia` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioAlumnoFisioterapia` VARCHAR(45) NULL DEFAULT NULL,
  `contraseñaAlumnoFisioterapia` VARCHAR(255) NULL DEFAULT NULL,
  `rfcProfesorFisioterapia_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`numeroCuentaAlumnoFisioterapia`),
  INDEX `FK_alumnoFisioterapia_profesorFisioterapia` (`rfcProfesorFisioterapia_FK` ASC) VISIBLE,
  INDEX `FK_alumnoFisioterapia_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_alumnoFisioterapia_profesorFisioterapia`
    FOREIGN KEY (`rfcProfesorFisioterapia_FK`)
    REFERENCES `serviciosocial`.`profesorfisioterapia` (`rfcProfesorFisioterapia`),
  CONSTRAINT `FK_alumnoFisioterapia_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`profesorodontologia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`profesorodontologia` (
  `rfcProfesorOdontologia` VARCHAR(45) NOT NULL,
  `nombreProfesorOdontologia` VARCHAR(45) NULL DEFAULT NULL,
  `apellidosProfesorOdontologia` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioProfesorOdontologia` VARCHAR(45) NOT NULL,
  `contraseñaProfesorOdontologia` VARCHAR(255) NOT NULL,
  `idAdminOdontologia_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`rfcProfesorOdontologia`),
  INDEX `FK_profesorOdontologia_adminOdontologia` (`idAdminOdontologia_FK` ASC) VISIBLE,
  INDEX `FK_profesorOdontologia_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_profesorOdontologia_adminOdontologia`
    FOREIGN KEY (`idAdminOdontologia_FK`)
    REFERENCES `serviciosocial`.`adminodontologia` (`idAdminOdontologia`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_profesorOdontologia_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`alumnoodontologia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`alumnoodontologia` (
  `numeroCuentaAlumnoOdontologia` VARCHAR(45) NOT NULL,
  `nombreAlumnoOdontologia` VARCHAR(45) NULL DEFAULT NULL,
  `apellidosAlumnoOdontologia` VARCHAR(45) NULL DEFAULT NULL,
  `año` VARCHAR(10) NULL DEFAULT NULL,
  `asignaturaAlumnoOdontologia` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioAlumnoOdontologia` VARCHAR(45) NOT NULL,
  `contraseñaAlumnoOdontologia` VARCHAR(255) NOT NULL,
  `rfcProfesorOdontologia_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`numeroCuentaAlumnoOdontologia`),
  INDEX `FK_alumnoOdontologia_profesorOdontologia` (`rfcProfesorOdontologia_FK` ASC) VISIBLE,
  INDEX `FK_alumnoOdontologia_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_alumnoOdontologia_profesorOdontologia`
    FOREIGN KEY (`rfcProfesorOdontologia_FK`)
    REFERENCES `serviciosocial`.`profesorodontologia` (`rfcProfesorOdontologia`),
  CONSTRAINT `FK_alumnoOdontologia_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`profesoroptometria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`profesoroptometria` (
  `rfcProfesorOptometria` VARCHAR(45) NOT NULL,
  `nombreProfesorOptometria` VARCHAR(45) NULL DEFAULT NULL,
  `apellidosProfesorOptometria` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioProfesorOptometria` VARCHAR(45) NOT NULL,
  `contraseñaProfesorOptometria` VARCHAR(255) NOT NULL,
  `idAdminOptometria_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`rfcProfesorOptometria`),
  INDEX `FK_profesorOptometria_adminOptometria` (`idAdminOptometria_FK` ASC) VISIBLE,
  INDEX `FK_profesorOptometria_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_profesorOptometria_adminOptometria`
    FOREIGN KEY (`idAdminOptometria_FK`)
    REFERENCES `serviciosocial`.`adminoptometria` (`idAdminOptometria`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_profesorOptometria_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`alumnooptometria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`alumnooptometria` (
  `numeroCuentaAlumnoOptometria` VARCHAR(45) NOT NULL,
  `nombreAlumnoOptometria` VARCHAR(45) NULL DEFAULT NULL,
  `apellidosAlumnoOptometria` VARCHAR(45) NULL DEFAULT NULL,
  `año` VARCHAR(10) NULL DEFAULT NULL,
  `asignaturaOptometria` VARCHAR(45) NULL DEFAULT NULL,
  `usuarioAlumnoOptometria` VARCHAR(45) NOT NULL,
  `contraseñaAlumnoOptometria` VARCHAR(255) NULL DEFAULT NULL,
  `rfcProfesorOptometria_FK` VARCHAR(45) NULL DEFAULT NULL,
  `idUsuario_FK` INT NULL DEFAULT NULL,
  PRIMARY KEY (`numeroCuentaAlumnoOptometria`),
  INDEX `FK_alumnoOptometria_profesorOptometria` (`rfcProfesorOptometria_FK` ASC) VISIBLE,
  INDEX `FK_alumnoOptometria_usuario_idx` (`idUsuario_FK` ASC) VISIBLE,
  CONSTRAINT `FK_alumnoOptometria_profesorOptometria`
    FOREIGN KEY (`rfcProfesorOptometria_FK`)
    REFERENCES `serviciosocial`.`profesoroptometria` (`rfcProfesorOptometria`),
  CONSTRAINT `FK_alumnoOptometria_usuario`
    FOREIGN KEY (`idUsuario_FK`)
    REFERENCES `serviciosocial`.`usuario` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`paciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`paciente` (
  `idPaciente` VARCHAR(10) NOT NULL,
  `rfcPaciente` VARCHAR(20) NULL DEFAULT NULL,
  `fechaRemision` DATE NULL DEFAULT NULL,
  `fechaAtención` DATE NULL DEFAULT NULL,
  `sexo` VARCHAR(20) NULL DEFAULT NULL,
  `edad` VARCHAR(20) NULL DEFAULT NULL,
  `nombrePaciente` VARCHAR(45) NULL DEFAULT NULL,
  `apellidoPaternoPaciente` VARCHAR(45) NULL DEFAULT NULL,
  `apellidoMaternoPaciente` VARCHAR(45) NULL DEFAULT NULL,
  `fechaNacimiento` DATE NULL DEFAULT NULL,
  `edadAños` VARCHAR(45) NULL DEFAULT NULL,
  `edadMeses` VARCHAR(45) NULL DEFAULT NULL,
  `telefonoCasa` VARCHAR(45) NULL DEFAULT NULL,
  `extensionTelefono` VARCHAR(45) NULL DEFAULT NULL,
  `telefonoOficina` VARCHAR(45) NULL DEFAULT NULL,
  `celular` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `calle` VARCHAR(45) NULL DEFAULT NULL,
  `numeroInterior` VARCHAR(45) NULL DEFAULT NULL,
  `numeroExterior` VARCHAR(45) NULL DEFAULT NULL,
  `colonia` VARCHAR(45) NULL DEFAULT NULL,
  `ciudad` VARCHAR(45) NULL DEFAULT NULL,
  `codigoPostal` VARCHAR(45) NULL DEFAULT NULL,
  `estado` VARCHAR(45) NULL DEFAULT NULL,
  `pais` VARCHAR(45) NULL DEFAULT NULL,
  `origen` VARCHAR(45) NULL DEFAULT NULL,
  `estadoCivil` VARCHAR(45) NULL DEFAULT NULL,
  `ocupacion` VARCHAR(45) NULL DEFAULT NULL,
  `nacionalidad` VARCHAR(45) NULL DEFAULT NULL,
  `tipoSangre` VARCHAR(45) NULL DEFAULT NULL,
  `clasificacion` VARCHAR(45) NULL DEFAULT NULL,
  `alertaAdministrativa` VARCHAR(45) NULL DEFAULT NULL,
  `numeroSeguro` VARCHAR(45) NULL DEFAULT NULL,
  `nombreContactoEmergencia` VARCHAR(45) NULL DEFAULT NULL,
  `telefonoContactoEmergencia` VARCHAR(45) NULL DEFAULT NULL,
  `coberturaMedica` VARCHAR(45) NULL DEFAULT NULL,
  `relacionContactoPaciente` VARCHAR(45) NULL DEFAULT NULL,
  `idAdminOdontologia_FK` VARCHAR(20) NULL DEFAULT NULL,
  `idAdminFisioterapia_FK` VARCHAR(20) NULL DEFAULT NULL,
  `idAdminOptometria_FK` VARCHAR(20) NULL DEFAULT NULL,
  `numeroCuentaAlumnoOdontologia_FK` VARCHAR(20) NULL DEFAULT NULL,
  `numeroCuentaAlumnoFisioterapia_FK` VARCHAR(20) NULL DEFAULT NULL,
  `numeroCuentaAlumnoOptometria_FK` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`idPaciente`),
  UNIQUE INDEX `rfcPaciente_UNIQUE` (`rfcPaciente` ASC) VISIBLE,
  INDEX `FK_paciente_adminOdontologia` (`idAdminOdontologia_FK` ASC) INVISIBLE,
  INDEX `FK_paciente_alumnoOdontologia` (`numeroCuentaAlumnoOdontologia_FK` ASC) INVISIBLE,
  INDEX `FK_paciente_adminFisioterapia` (`idAdminFisioterapia_FK` ASC) VISIBLE,
  INDEX `FK_paciente_alumnoFisioterapia` (`numeroCuentaAlumnoFisioterapia_FK` ASC) VISIBLE,
  INDEX `FK_paciente_adminOptometria` (`idAdminOptometria_FK` ASC) VISIBLE,
  INDEX `FK_paciente_alumnoOptometria` (`numeroCuentaAlumnoOptometria_FK` ASC) VISIBLE,
  CONSTRAINT `FK_paciente_adminFisioterapia`
    FOREIGN KEY (`idAdminFisioterapia_FK`)
    REFERENCES `serviciosocial`.`adminfisioterapia` (`idAdminFisioterapia`),
  CONSTRAINT `FK_paciente_adminOdontologia`
    FOREIGN KEY (`idAdminOdontologia_FK`)
    REFERENCES `serviciosocial`.`adminodontologia` (`idAdminOdontologia`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_paciente_adminOptometria`
    FOREIGN KEY (`idAdminOptometria_FK`)
    REFERENCES `serviciosocial`.`adminoptometria` (`idAdminOptometria`),
  CONSTRAINT `FK_paciente_alumnoFisioterapia`
    FOREIGN KEY (`numeroCuentaAlumnoFisioterapia_FK`)
    REFERENCES `serviciosocial`.`alumnofisioterapia` (`numeroCuentaAlumnoFisioterapia`),
  CONSTRAINT `FK_paciente_alumnoOdontologia`
    FOREIGN KEY (`numeroCuentaAlumnoOdontologia_FK`)
    REFERENCES `serviciosocial`.`alumnoodontologia` (`numeroCuentaAlumnoOdontologia`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_paciente_alumnoOptometria`
    FOREIGN KEY (`numeroCuentaAlumnoOptometria_FK`)
    REFERENCES `serviciosocial`.`alumnooptometria` (`numeroCuentaAlumnoOptometria`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`fisioterapia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`fisioterapia` (
  `idFisioterapia` INT NOT NULL AUTO_INCREMENT,
  `idPaciente` VARCHAR(45) NULL DEFAULT NULL,
  `octDiscoOptico` VARCHAR(80) NULL DEFAULT NULL,
  `octMacular` VARCHAR(80) NULL DEFAULT NULL,
  `octMacularCube` VARCHAR(80) NULL DEFAULT NULL,
  `octA` VARCHAR(80) NULL DEFAULT NULL,
  `anguloIridocorneal` VARCHAR(80) NULL DEFAULT NULL,
  `proximaVisita` VARCHAR(45) NULL DEFAULT NULL,
  `idPaciente_FK` VARCHAR(45) NULL,
  PRIMARY KEY (`idFisioterapia`),
  INDEX `FK_fisioterapia_paciente_idx` (`idPaciente` ASC) VISIBLE,
  CONSTRAINT `FK_fisioterapia_paciente`
    FOREIGN KEY (`idPaciente`)
    REFERENCES `serviciosocial`.`paciente` (`idPaciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`odontologia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`odontologia` (
  `idOdontologia` INT NOT NULL AUTO_INCREMENT,
  `idPaciente` VARCHAR(45) NULL DEFAULT NULL,
  `octDiscoOptico` VARCHAR(80) NULL DEFAULT NULL,
  `octMacular` VARCHAR(80) NULL DEFAULT NULL,
  `octMacularCube` VARCHAR(80) NULL DEFAULT NULL,
  `octA` VARCHAR(80) NULL DEFAULT NULL,
  `anguloIridocorneal` VARCHAR(80) NULL DEFAULT NULL,
  `proximaVisita` VARCHAR(45) NULL DEFAULT NULL,
  `idPaciente_FK` VARCHAR(45) NULL,
  PRIMARY KEY (`idOdontologia`),
  INDEX `FK_odontologia_paciente_idx` (`idPaciente` ASC) VISIBLE,
  CONSTRAINT `FK_odontologia_paciente`
    FOREIGN KEY (`idPaciente`)
    REFERENCES `serviciosocial`.`paciente` (`idPaciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `serviciosocial`.`optometria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `serviciosocial`.`optometria` (
  `idOptometria` INT NOT NULL AUTO_INCREMENT,
  `idPaciente` VARCHAR(45) NULL DEFAULT NULL,
  `octDiscoOptico` VARCHAR(80) NULL DEFAULT NULL,
  `octMacular` VARCHAR(80) NULL DEFAULT NULL,
  `octMacularCube` VARCHAR(80) NULL DEFAULT NULL,
  `octA` VARCHAR(80) NULL DEFAULT NULL,
  `anguloIridocorneal` VARCHAR(80) NULL DEFAULT NULL,
  `retinografiaPosiciones` VARCHAR(80) NULL DEFAULT NULL,
  `retinografiaCentral` VARCHAR(80) NULL DEFAULT NULL,
  `ergBasal` VARCHAR(80) NULL DEFAULT NULL,
  `ergPhNR` VARCHAR(80) NULL DEFAULT NULL,
  `ergRD` VARCHAR(80) NULL DEFAULT NULL,
  `ergFlickerThenFlash` VARCHAR(80) NULL DEFAULT NULL,
  `contrastSensitivity` VARCHAR(45) NULL DEFAULT NULL,
  `tonometria` VARCHAR(45) NULL DEFAULT NULL,
  `campimetriaFast` VARCHAR(80) NULL DEFAULT NULL,
  `topografia` VARCHAR(80) NULL DEFAULT NULL,
  `estudiosClinicos` VARCHAR(80) NULL DEFAULT NULL,
  `OSDI` VARCHAR(45) NULL DEFAULT NULL,
  `BUT` VARCHAR(45) NULL DEFAULT NULL,
  `schirmer` VARCHAR(45) NULL DEFAULT NULL,
  `pesoCorporal` VARCHAR(45) NULL DEFAULT NULL,
  `estatura` VARCHAR(45) NULL DEFAULT NULL,
  `circunferenciaCintura` VARCHAR(45) NULL DEFAULT NULL,
  `IMC` VARCHAR(45) NULL DEFAULT NULL,
  `genero` VARCHAR(45) NULL DEFAULT NULL,
  `edad` VARCHAR(45) NULL DEFAULT NULL,
  `paquimetria` VARCHAR(45) NULL DEFAULT NULL,
  `glucosa` VARCHAR(45) NULL DEFAULT NULL,
  `presiónArterial` VARCHAR(45) NULL DEFAULT NULL,
  `diagnosticoOcular` VARCHAR(45) NULL DEFAULT NULL,
  `tratamientos` VARCHAR(45) NULL DEFAULT NULL,
  `seguimiento` VARCHAR(45) NULL DEFAULT NULL,
  `proximaVisita` VARCHAR(45) NULL DEFAULT NULL,
  `idPaciente_FK` VARCHAR(45) NULL,
  PRIMARY KEY (`idOptometria`),
  INDEX `FK_optometria_paciente_idx` (`idPaciente` ASC) VISIBLE,
  CONSTRAINT `FK_optometria_paciente`
    FOREIGN KEY (`idPaciente`)
    REFERENCES `serviciosocial`.`paciente` (`idPaciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

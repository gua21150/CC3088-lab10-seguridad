CREATE TABLE estudiante(
    id_est          INT PRIMARY KEY, -- realiza una llave autoincrementada
    fechaNacimiento DATE,
    nombres         VARCHAR(50),
    apellidos       VARCHAR(50)
);

CREATE TABLE curso(
    id              INT PRIMARY KEY, -- llave autoincrementada
    cod_curso       VARCHAR(25) UNIQUE, -- CC3088, MM2018
    nombre          VARCHAR(50),
    cupo_actual     INTEGER,
    cupo_max        INTEGER
);

CREATE TABLE asignacion(
    id_est          INT,
    id_Curso        INT,
    fechaAsignacion DATE,
    CONSTRAINT fk_est FOREIGN KEY(id_est) REFERENCES estudiante(id_est) 
                                       ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_id_Curso FOREIGN KEY(id_Curso) REFERENCES curso(id)
                                       ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT idAsignacion UNIQUE(id_est, id_Curso, fechaAsignacion)
);

-- Data Control Language

-- Creación de roles/grupos
CREATE ROLE admin_nivel1;
CREATE ROLE admin_nivel2;
CREATE ROLE admin_nivel3;

-- Dar permisos a los roles para realizar login
GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA public TO admin_nivel1;

GRANT INSERT ON estudiante, curso TO admin_nivel2;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO admin_nivel3;
GRANT INSERT ON asignacion TO admin_nivel3;
-- Crear usuarios
CREATE USER diana1 WITH PASSWORD 'nice';
CREATE USER mariel1 WITH PASSWORD 'chido';
CREATE USER diana2 WITH PASSWORD 'nice';
CREATE USER mariel2 WITH PASSWORD 'chido';
CREATE USER diana3 WITH PASSWORD 'nice';
CREATE USER mariel3 WITH PASSWORD 'chido';
-- Crear grupos de usuarios que tiene las caracteristicas de roles
CREATE GROUP admin1 WITH USER diana1, mariel1;
CREATE GROUP admin2 WITH USER diana2, mariel2;
CREATE GROUP admin3 WITH USER diana3, mariel3;
-- Dar privilegios a grupos (ingresarlos a rol)
GRANT  admin_nivel1 TO admin1;
GRANT  admin_nivel2 TO admin2;
GRANT  admin_nivel3 TO admin3;


-- Modifique el grupo admin_nivel1 (admin1), colóquele una contraseña que expire en cierto momento del día. 
ALTER ROLE admin1 WITH LOGIN;
ALTER ROLE admin1 PASSWORD 'temp' VALID UNTIL 'November 5 16:35:00 2022';
-- Modificar a usuario dentro de rol admin_nivel1
ALTER ROLE admin1 WITH NOLOGIN;
ALTER ROLE admin1 WITH PASSWORD null;
ALTER USER diana1 WITH PASSWORD 'increible' VALID UNTIL 'November 5 16:45:00 2022'

    
-- Modificar al grupo (rol) admin_nivel3 otórguele el privilegio de CREATE sobre la tabla estudiantes
GRANT INSERT ON estudiante TO admin_nivel3;



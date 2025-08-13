CREATE DATABASE sistema_racks;
USE sistema_racks;

CREATE TABLE Blocos (
	id_bloco INT PRIMARY KEY AUTO_INCREMENT,
	nome_bloco VARCHAR(100)
);

CREATE TABLE Racks (
	id_rack INT PRIMARY KEY AUTO_INCREMENT,
    num_patrimonio INT UNIQUE,
    capacidade_u INT,
    sala VARCHAR(50),
    id_bloco_blocos INT NOT NULL, 
    FOREIGN KEY (id_bloco_blocos) REFERENCES Blocos(id_bloco)
);

CREATE TABLE Switch (
	id_switch INT PRIMARY KEY AUTO_INCREMENT,
    quantidade_portas INT(2) NOT NULL,
    num_patrimonio INT UNIQUE,
    id_rack_racks INT NOT NULL,
    FOREIGN KEY (id_rack_racks) REFERENCES Racks(id_rack)
);

CREATE TABLE Portas (
	id_porta INT(2) PRIMARY KEY,
    id_switch_switch INT NOT NULL,
    FOREIGN KEY (id_switch_switch) REFERENCES Switch(id_switch)
);

CREATE TABLE Historico (
	id_historico INT PRIMARY KEY AUTO_INCREMENT,
    acao VARCHAR(255) NOT NULL,
    observacao TEXT 
);
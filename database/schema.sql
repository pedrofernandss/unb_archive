CREATE TABLE Reputacao (
    id_reputacao SERIAL PRIMARY KEY,
    pontuacao INTEGER NOT NULL,
    nivel VARCHAR(20)
);

CREATE TABLE Universidade (
    ies SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2)
);

CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    id_universidade INTEGER NOT NULL,
    FOREIGN KEY (id_universidade) REFERENCES Universidade(ies)
);

CREATE TABLE Curso (
    curso VARCHAR(100),
    departamento_curso INTEGER,
    PRIMARY KEY (curso, departamento_curso),
    FOREIGN KEY (departamento_curso) REFERENCES Departamento(id_departamento)
);

CREATE TABLE Escolaridade (
    escolaridade VARCHAR(100),
    departamento_escolaridade INTEGER,
    PRIMARY KEY (escolaridade, departamento_escolaridade),
    FOREIGN KEY (departamento_escolaridade) REFERENCES Departamento(id_departamento)
);

CREATE TABLE Usuario (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    id_departamento INTEGER NOT NULL,
    matricula VARCHAR(20),
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento)
);

CREATE TABLE Discente (
    id_usuario_discente VARCHAR(14) PRIMARY KEY,
    ano_ingresso INTEGER,
    status VARCHAR(20),
    coeficiente_rendimento NUMERIC(4,2),
    id_reputacao INTEGER,
    FOREIGN KEY (id_usuario_discente) REFERENCES Usuario(cpf),
    FOREIGN KEY (id_reputacao) REFERENCES Reputacao(id_reputacao)
);

CREATE TABLE Docente (
    id_usuario_docente VARCHAR(14) PRIMARY KEY,
    especialidade VARCHAR(100),
    qnt_validacoes INTEGER DEFAULT 0,
    qnt_marcacoes_inapropriadas INTEGER DEFAULT 0,
    permissao_validacao BOOLEAN
);

CREATE TABLE Disciplina (
    codigo SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    id_departamento INTEGER NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento)
);

CREATE TABLE Material (
    id_material SERIAL PRIMARY KEY,
    nome VARCHAR(200),
    descricao TEXT,
    ano_semestre_ref VARCHAR(10),
    local_arquivo BYTEA,
    id_disciplina INTEGER,
    FOREIGN KEY (id_disciplina) REFERENCES Disciplina(codigo)
);

CREATE TABLE Avaliacao (
    id_avaliacao SERIAL PRIMARY KEY,
    data_avaliacao DATE,
    nota NUMERIC(3,1),
    id_material INTEGER NOT NULL,
    FOREIGN KEY (id_material) REFERENCES Material(id_material)
);

CREATE TABLE Avalia (
    id_avalia SERIAL PRIMARY KEY,
    id_docente VARCHAR(14),
    id_material INTEGER,
    valido BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_docente) REFERENCES Docente(id_usuario_docente),
    FOREIGN KEY (id_material) REFERENCES Material(id_material)
);

ALTER TABLE Docente ADD COLUMN idAvalia INTEGER;
ALTER TABLE Docente ADD FOREIGN KEY (idAvalia) REFERENCES Avalia(id_avalia);

ALTER TABLE Material ADD COLUMN idAvalia INTEGER;
ALTER TABLE Material ADD FOREIGN KEY (idAvalia) REFERENCES Avalia(id_avalia);

CREATE TABLE Compartilha_Produz (
    id_material INTEGER,
    id_docente VARCHAR(14),
    PRIMARY KEY (id_material, id_docente),
    FOREIGN KEY (id_material) REFERENCES Material(id_material),
    FOREIGN KEY (id_docente) REFERENCES Docente(id_usuario_docente)
);

CREATE TABLE Tag (
    id_tag SERIAL PRIMARY KEY,
    nome_tag VARCHAR(50) NOT NULL
);

CREATE TABLE Possui (
    id_material INTEGER,
    id_tag INTEGER,
    PRIMARY KEY (id_material, id_tag),
    FOREIGN KEY (id_material) REFERENCES Material(id_material),
    FOREIGN KEY (id_tag) REFERENCES Tag(id_tag)
);
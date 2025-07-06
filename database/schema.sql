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
    FOREIGN KEY (id_universidade) REFERENCES Universidade(ies) ON DELETE CASCADE
);

CREATE TABLE Curso (
    curso VARCHAR(100),
    departamento_curso INTEGER,
    PRIMARY KEY (curso, departamento_curso),
    FOREIGN KEY (departamento_curso) REFERENCES Departamento(id_departamento) ON DELETE CASCADE
);

CREATE TABLE Escolaridade (
    escolaridade VARCHAR(100),
    departamento_escolaridade INTEGER,
    PRIMARY KEY (escolaridade, departamento_escolaridade),
    FOREIGN KEY (departamento_escolaridade) REFERENCES Departamento(id_departamento) ON DELETE CASCADE
);

CREATE TABLE Usuario (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    id_universidade INTEGER NOT NULL,
    id_departamento INTEGER NOT NULL,
    matricula VARCHAR(20),
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento) ON DELETE CASCADE,
    FOREIGN KEY (id_universidade) REFERENCES Universidade(ies) ON DELETE CASCADE
);

CREATE TABLE Discente (
    id_usuario_discente VARCHAR(14) PRIMARY KEY,
    ano_ingresso INTEGER,
    status VARCHAR(20),
    coeficiente_rendimento NUMERIC(4,2),
    id_reputacao INTEGER,
    FOREIGN KEY (id_usuario_discente) REFERENCES Usuario(cpf) ON DELETE CASCADE,
    FOREIGN KEY (id_reputacao) REFERENCES Reputacao(id_reputacao) ON DELETE SET NULL
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
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento) ON DELETE CASCADE
);

CREATE TABLE Material (
    id_material SERIAL PRIMARY KEY,
    nome VARCHAR(200),
    descricao TEXT,
    ano_semestre_ref VARCHAR(10),
    local_arquivo BYTEA,
    id_disciplina INTEGER,
    FOREIGN KEY (id_disciplina) REFERENCES Disciplina(codigo) ON DELETE CASCADE
);

CREATE TABLE Avaliacao (
    id_avaliacao SERIAL PRIMARY KEY,
    data_avaliacao DATE,
    nota NUMERIC(3,1),
    id_material INTEGER NOT NULL,
    FOREIGN KEY (id_material) REFERENCES Material(id_material) ON DELETE CASCADE
);

CREATE TABLE Avalia (
    id_avalia SERIAL PRIMARY KEY,
    id_docente VARCHAR(14),
    id_material INTEGER,
    valido BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_docente) REFERENCES Docente(id_usuario_docente) ON DELETE CASCADE,
    FOREIGN KEY (id_material) REFERENCES Material(id_material) ON DELETE CASCADE
);

ALTER TABLE Docente ADD COLUMN id_avalia INTEGER;
ALTER TABLE Docente ADD FOREIGN KEY (id_avalia) REFERENCES Avalia(id_avalia) ON DELETE SET NULL;

ALTER TABLE Material ADD COLUMN id_avalia INTEGER;
ALTER TABLE Material ADD FOREIGN KEY (id_avalia) REFERENCES Avalia(id_avalia) ON DELETE SET NULL;

CREATE TABLE Compartilha_Produz (
    id_material INTEGER,
    id_docente VARCHAR(14),
    PRIMARY KEY (id_material, id_docente),
    FOREIGN KEY (id_material) REFERENCES Material(id_material) ON DELETE CASCADE,
    FOREIGN KEY (id_docente) REFERENCES Docente(id_usuario_docente) ON DELETE CASCADE
);

CREATE TABLE Tag (
    id_tag SERIAL PRIMARY KEY,
    nome_tag VARCHAR(50) NOT NULL
);

CREATE TABLE Possui (
    id_material INTEGER,
    id_tag INTEGER,
    PRIMARY KEY (id_material, id_tag),
    FOREIGN KEY (id_material) REFERENCES Material(id_material) ON DELETE CASCADE,
    FOREIGN KEY (id_tag) REFERENCES Tag(id_tag) ON DELETE CASCADE
);

-- 3. Criação da View
CREATE VIEW vw_materiais_completos AS
SELECT 
    m.id_material,
    m.nome AS material_nome,
    m.descricao,
    m.ano_semestre_ref,
    d.nome AS disciplina_nome,
    dep.nome AS departamento_nome,
    u.nome AS universidade_nome,
    u.cidade,
    u.estado,
    COALESCE(AVG(av.nota), 0) AS media_avaliacoes,
    COALESCE(COUNT(av.id_avaliacao), 0) AS total_avaliacoes,
    STRING_AGG(DISTINCT doc_usuario.nome, ', ') AS docentes_associados,
    STRING_AGG(DISTINCT tg.nome_tag, ', ') AS tags
FROM Material m
INNER JOIN Disciplina d ON m.id_disciplina = d.codigo
INNER JOIN Departamento dep ON d.id_departamento = dep.id_departamento
INNER JOIN Universidade u ON dep.id_universidade = u.ies
LEFT JOIN Avaliacao av ON m.id_material = av.idMaterial
LEFT JOIN Compartilha_Produz cp ON m.id_material = cp.id_material
LEFT JOIN Docente doc ON cp.id_docente = doc.id_usuario_docente
LEFT JOIN Usuario doc_usuario ON doc.id_usuario_docente = doc_usuario.cpf
LEFT JOIN Possui p ON m.id_material = p.id_material
LEFT JOIN Tag tg ON p.id_tag = tg.id_tag
GROUP BY 
    m.id_material,
    m.nome,
    m.descricao,
    m.ano_semestre_ref,
    d.nome,
    dep.nome,
    u.nome,
    u.cidade,
    u.estado;
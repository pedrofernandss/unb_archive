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
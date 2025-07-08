CREATE OR REPLACE VIEW vw_materiais_completos AS
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
    STRING_AGG(DISTINCT usr.nome, ', ') AS usuarios_associados,
    STRING_AGG(DISTINCT tg.nome_tag, ', ') AS tags
FROM Material m
INNER JOIN Disciplina d ON m.id_disciplina = d.codigo
INNER JOIN Departamento dep ON d.id_departamento = dep.id_departamento
INNER JOIN Universidade u ON dep.id_universidade = u.ies
LEFT JOIN Avaliacao av ON m.id_material = av.id_material
LEFT JOIN Compartilha_Produz cp ON m.id_material = cp.id_material
LEFT JOIN Usuario usr ON cp.cpf_usuario = usr.cpf
LEFT JOIN Possui p ON m.id_material = p.id_material
LEFT JOIN Tag tg ON p.id_tag = tg.id_tag
GROUP BY 
    m.id_material,
    d.nome,
    dep.nome,
    u.nome,
    u.cidade,
    u.estado;


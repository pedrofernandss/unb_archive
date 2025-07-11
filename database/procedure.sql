CREATE OR REPLACE PROCEDURE gerenciar_validacao_material(
    p_id_material INTEGER,
    p_cpf_docente VARCHAR,
    p_acao_valida BOOLEAN
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_permissao_validacao BOOLEAN;
    v_docente_existe BOOLEAN;
    v_material_existe BOOLEAN;
    v_id_reputacao_discente INTEGER;
    v_pontuacao_atual INTEGER;
    v_nivel_atual VARCHAR;
    v_cpf_discente VARCHAR(14);
    v_qnt_marcacoes INTEGER;
BEGIN
    -- 1. Verificar se o docente existe e tem permissão para validar
    SELECT permissao_validacao, TRUE INTO v_permissao_validacao, v_docente_existe
    FROM Docente
    WHERE id_usuario_docente = p_cpf_docente;

    IF NOT v_docente_existe THEN
        RAISE EXCEPTION 'Docente com CPF % não encontrado.', p_cpf_docente;
    END IF;

    IF NOT v_permissao_validacao THEN
        RAISE EXCEPTION 'Docente com CPF % não tem permissão para validar materiais.', p_cpf_docente;
    END IF;

    -- 2. Verificar se o material existe
    SELECT EXISTS(SELECT 1 FROM Material WHERE id_material = p_id_material) INTO v_material_existe;

    IF NOT v_material_existe THEN
        RAISE EXCEPTION 'Material com ID % não encontrado.', p_id_material;
    END IF;

    -- 3. Inserir ou atualizar o registro na tabela Avalia (UPSERT)
    INSERT INTO Avalia (id_docente, id_material, valido)
    VALUES (p_cpf_docente, p_id_material, p_acao_valida)
    ON CONFLICT (id_docente, id_material) 
    DO UPDATE SET valido = EXCLUDED.valido;

    -- 4. Atualizar contadores do docente
    IF p_acao_valida THEN
        UPDATE Docente SET qnt_validacoes = qnt_validacoes + 1 WHERE id_usuario_docente = p_cpf_docente;
    ELSE
        UPDATE Docente SET qnt_marcacoes_inapropriadas = qnt_marcacoes_inapropriadas + 1 WHERE id_usuario_docente = p_cpf_docente;
        
        -- Verificar se as marcações excedem o limite e revogar permissão
        SELECT qnt_marcacoes_inapropriadas INTO v_qnt_marcacoes FROM Docente WHERE id_usuario_docente = p_cpf_docente;
        
        IF v_qnt_marcacoes > 10 THEN
            UPDATE Docente SET permissao_validacao = FALSE WHERE id_usuario_docente = p_cpf_docente;
            RAISE NOTICE 'Permissão de validação revogada para o docente %.', p_cpf_docente;
        END IF;
    END IF;

    -- 5. Impactar a reputação do discente que postou o material
    SELECT cpf_usuario INTO v_cpf_discente
    FROM Compartilha_Produz
    WHERE id_material = p_id_material
    LIMIT 1; 

    -- Verifica se o usuário encontrado é um discente
    IF v_cpf_discente IS NOT NULL AND EXISTS(SELECT 1 FROM Discente WHERE id_usuario_discente = v_cpf_discente) THEN
        
        -- Obtém a reputação atual do discente
        SELECT r.pontuacao, r.nivel, d.id_reputacao INTO v_pontuacao_atual, v_nivel_atual, v_id_reputacao_discente
        FROM Reputacao r
        JOIN Discente d ON r.id_reputacao = d.id_reputacao
        WHERE d.id_usuario_discente = v_cpf_discente;

        IF v_id_reputacao_discente IS NOT NULL THEN
            IF p_acao_valida THEN
                v_pontuacao_atual := v_pontuacao_atual + 10;
            ELSE
                v_pontuacao_atual := v_pontuacao_atual - 5;
            END IF;

            IF v_pontuacao_atual < 0 THEN
                v_pontuacao_atual := 0;
            END IF;

            IF v_pontuacao_atual >= 100 THEN v_nivel_atual := 'Expert';
            ELSIF v_pontuacao_atual >= 50 THEN v_nivel_atual := 'Avançado';
            ELSIF v_pontuacao_atual >= 10 THEN v_nivel_atual := 'Intermediário';
            ELSE v_nivel_atual := 'Básico';
            END IF;

            UPDATE Reputacao
            SET pontuacao = v_pontuacao_atual, nivel = v_nivel_atual
            WHERE id_reputacao = v_id_reputacao_discente;
        END IF;
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Ocorreu um erro no procedimento: %', SQLERRM;
        RAISE;
END;
$$;

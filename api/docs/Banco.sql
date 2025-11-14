CREATE DATABASE IF NOT EXISTS projeto;
USE projeto;

-- Tabela de Usuários (ATUALIZADA)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    empresa VARCHAR(255) NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Projetos (ATUALIZADA com usuário)
CREATE TABLE IF NOT EXISTS projetos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_inicio DATETIME NULL,
    data_fim DATETIME NULL,
    status VARCHAR(50) DEFAULT 'pendente',
    usuario_id INT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_id (usuario_id)
);

-- Tabela de Tarefas (ATUALIZADA com responsável e atribuidor)
CREATE TABLE IF NOT EXISTS tarefas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'pendente',
    prioridade VARCHAR(50) DEFAULT 'media',
    concluida BOOLEAN DEFAULT FALSE,
    data_limite DATETIME NULL,
    data_inicio DATETIME NULL,
    data_fim DATETIME NULL,
    projeto_id INT NOT NULL,
    
    -- ✅ NOVOS CAMPOS: Responsável pela tarefa e quem atribuiu
    usuario_responsavel_id INT NOT NULL,  -- Usuário RESPONSÁVEL pela execução da tarefa
    usuario_atribuidor_id INT NOT NULL,   -- Usuário que ATRIBUIU a tarefa
    
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Chaves estrangeiras
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_responsavel_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_atribuidor_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    
    -- Índices para performance
    INDEX idx_usuario_responsavel (usuario_responsavel_id),
    INDEX idx_usuario_atribuidor (usuario_atribuidor_id),
    INDEX idx_projeto_id (projeto_id),
    INDEX idx_status (status),
    INDEX idx_prioridade (prioridade)
);

-- Inserir dados de exemplo (ATUALIZADO)
INSERT INTO usuarios (nome, email, senha_hash, empresa) VALUES
('Ana Silva', 'ana.silva@email.com', '$2b$12$LQv3c1yqBWVHxkd0g8f/sOe1e8QGk5R5Vc8Vv7v8B8k8kX8v8B8k8', 'Tech Solutions'),
('Bruno Costa', 'bruno.costa@email.com', '$2b$12$LQv3c1yqBWVHxkd0g8f/sOe1e8QGk5R5Vc8Vv7v8B8k8kX8v8B8k8', 'Mobile Dev Inc'),
('Carlos Oliveira', 'carlos.oliveira@email.com', '$2b$12$LQv3c1yqBWVHxkd0g8f/sOe1e8QGk5R5Vc8Vv7v8B8k8kX8v8B8k8', 'Web Masters'),
('Davi Santos', 'davi@email.com', '$2b$12$LQv3c1yqBWVHxkd0g8f/sOe1e8QGk5R5Vc8Vv7v8B8k8kX8v8B8k8', NULL);

-- Inserir projetos (AGORA CADA USUÁRIO TEM SEUS PRÓPRIOS PROJETOS)
INSERT INTO projetos (nome, descricao, data_inicio, data_fim, status, usuario_id) VALUES
-- Projetos da Ana (usuário 1)
('API de E-commerce', 'Desenvolver a API REST para a nova loja virtual.', '2025-11-01 09:00:00', '2025-12-15 18:00:00', 'andamento', 1),
('Website Institucional', 'Criar o novo site da empresa com um blog integrado.', '2025-10-20 08:30:00', '2025-11-10 17:00:00', 'concluido', 1),

-- Projetos do Bruno (usuário 2)
('Aplicativo Mobile de Fitness', 'App para iOS e Android para monitoramento de treinos.', '2026-01-15 10:00:00', '2026-03-20 18:00:00', 'pendente', 2),
('Sistema de Gestão', 'Sistema interno para gestão de processos.', '2025-11-01 08:00:00', '2025-12-01 18:00:00', 'andamento', 2),

-- Projetos do Carlos (usuário 3)
('Portal de Notícias', 'Desenvolvimento de portal de notícias com CMS.', '2025-11-10 09:00:00', '2025-12-20 18:00:00', 'pendente', 3),

-- Projetos do Davi (usuário 4)
('Blog Pessoal', 'Meu blog pessoal sobre tecnologia.', '2025-11-05 10:00:00', NULL, 'andamento', 4);

-- Inserir tarefas (AGORA COM RESPONSÁVEL E ATRIBUIDOR)
INSERT INTO tarefas (titulo, descricao, status, prioridade, concluida, data_limite, data_inicio, data_fim, projeto_id, usuario_responsavel_id, usuario_atribuidor_id) VALUES
-- ✅ Tarefas onde Ana (usuário 1) é responsável
('Definir endpoints de produtos', 'Definir todos os endpoints da API de produtos', 'concluida', 'alta', TRUE, '2025-11-05 18:00:00', '2025-11-01 09:00:00', '2025-11-03 17:00:00', 1, 1, 1),
('Implementar autenticação JWT', 'Desenvolver sistema de autenticação JWT', 'andamento', 'alta', FALSE, '2025-11-10 18:00:00', '2025-11-04 09:00:00', NULL, 1, 1, 2), -- Atribuída por Bruno

-- ✅ Tarefas onde Bruno (usuário 2) é responsável
('Criar CRUD de clientes', 'Implementar operações CRUD para clientes', 'pendente', 'media', FALSE, '2025-11-15 18:00:00', NULL, NULL, 1, 2, 1), -- Atribuída por Ana
('Desenhar telas no Figma', 'Criar protótipo das telas do aplicativo', 'andamento', 'alta', FALSE, '2026-01-30 18:00:00', '2026-01-15 10:00:00', NULL, 3, 2, 2),
('Configurar ambiente React Native', 'Configurar ambiente de desenvolvimento', 'pendente', 'media', FALSE, '2026-02-05 18:00:00', NULL, NULL, 3, 2, 3), -- Atribuída por Carlos

-- ✅ Tarefas onde Carlos (usuário 3) é responsável
('Definir estrutura do banco', 'Criar modelo de dados do portal', 'pendente', 'alta', FALSE, '2025-11-15 18:00:00', NULL, NULL, 5, 3, 3),
('Desenvolver template principal', 'Criar template base do portal', 'pendente', 'media', FALSE, '2025-11-20 18:00:00', NULL, NULL, 5, 3, 4), -- Atribuída por Davi

-- ✅ Tarefas onde Davi (usuário 4) é responsável
('Escolher tema do blog', 'Selecionar tema WordPress para o blog', 'concluida', 'baixa', TRUE, '2025-11-06 18:00:00', '2025-11-05 10:00:00', '2025-11-05 16:00:00', 6, 4, 4),
('Escrever primeiro artigo', 'Artigo sobre Flask e MySQL', 'andamento', 'alta', FALSE, '2025-11-12 18:00:00', '2025-11-06 09:00:00', NULL, 6, 4, 1), -- Atribuída por Ana

-- ✅ Tarefas com diferentes combinações de responsável/atribuidor
('Revisar código da API', 'Revisar código dos endpoints implementados', 'pendente', 'alta', FALSE, '2025-11-08 18:00:00', NULL, NULL, 1, 3, 1), -- Carlos responsável, Ana atribuiu
('Testar funcionalidades', 'Realizar testes das funcionalidades implementadas', 'pendente', 'media', FALSE, '2025-11-09 18:00:00', NULL, NULL, 1, 4, 2), -- Davi responsável, Bruno atribuiu
('Documentar API', 'Criar documentação completa da API', 'pendente', 'baixa', FALSE, '2025-11-20 18:00:00', NULL, NULL, 1, 2, 3); -- Bruno responsável, Carlos atribuiu
